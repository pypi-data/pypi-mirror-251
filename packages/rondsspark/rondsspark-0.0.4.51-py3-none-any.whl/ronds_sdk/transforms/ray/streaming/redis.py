import copy
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List

import ujson

from ronds_sdk import logger_config, error
from ronds_sdk.datasources.redis_manager import RedisManager
from ronds_sdk.models.graph import ExceptionExe, Graph, DeviceModel
from ronds_sdk.tools import utils
from ronds_sdk.tools.constants import JsonKey
from ronds_sdk.tools.data_utils import DataUtils
from ronds_sdk.tools.graph_utils import GraphUtils
from ronds_sdk.transforms.ray.base import RayTransform

if TYPE_CHECKING:
    from ronds_sdk.options.pipeline_options import PipelineOptions

logger = logger_config.config()


class RuleReadRedisBuffer(RayTransform):
    def __init__(self,  # type: RuleReadRedisBuffer
                 key_prefix=None,  # type: str
                 options=None,  # type: Optional[PipelineOptions]
                 parallel=None,  # type: Optional[int]
                 num_cpus=0.5,  # type: float
                 num_gpus=0,  # type: float
                 worker_index=-1,  # type: int
                 ):
        # type: (...) -> None
        super().__init__(worker_index,
                         parallel=parallel,
                         num_cpus=num_cpus,
                         num_gpus=num_gpus,
                         options=options)
        self.key_prefix = key_prefix
        self._redis_manager = None  # type: Optional[RedisManager]

    def pre_startup(self):
        super().pre_startup()
        if self.key_prefix is None:
            self.key_prefix = self.options.get_pipeline_namespace()
        logger.info("key_prefix: %s", self.key_prefix)
        self._redis_manager = RedisManager(self.options)

    @property
    def redis_manager(self):
        return self._redis_manager

    async def process(self, inputs):
        # type: ('RuleReadRedisBuffer', dict[str, str|List[str]]) -> str|List[str]|None
        for p_name, record_str in inputs.items():
            record = ujson.loads(record_str)
            row_key = get_row_key(self.key_prefix, record)
            value_node = record[JsonKey.MESSAGE.value]  # type: Optional[dict]
            cache = self.get_redis_buffer(row_key, record[JsonKey.ID.value])
            has_empty_cached = 'cache' in value_node \
                               and utils.collection_empty(value_node['cache']['metadata'])
            if utils.collection_empty(cache['metadata']) and has_empty_cached:
                yield record_str
            else:
                value_node['cache'] = cache
                yield ujson.dumps(record)

    def get_redis_buffer(self, row_key, did):
        """
        根据 row_key 获取 redis 缓存
        :param row_key: row key
        :param did: id
        :return: buffer dict
        """
        buffer = self.redis_manager.get(row_key)
        return ujson.loads(buffer) if utils.is_not_blank(buffer) \
            else {
            JsonKey.DEVICE_ID.value: did,
            "metadata": [],
            "buffer": ""
        }


class RedisReadDevModelAndDynaPara(RayTransform):
    def __init__(self,  # type: RedisReadDevModelAndDynaPara
                 options=None,  # type: Optional[PipelineOptions]
                 parallel=None,  # type: Optional[int]
                 num_cpus=0.5,  # type: float
                 num_gpus=0,  # type: float
                 worker_index=-1,  # type: int
                 ):
        # type: (...) -> None
        super().__init__(worker_index,
                         parallel=parallel,
                         num_cpus=num_cpus,
                         num_gpus=num_gpus,
                         options=options)
        self._redis_manager = None  # type: Optional[RedisManager]

    def pre_startup(self):
        super().pre_startup()
        self._redis_manager = RedisManager(self.options)

    @property
    def redis_manager(self):
        return self._redis_manager

    # noinspection SpellCheckingInspection
    async def process(self, inputs):
        # type: ('RedisReadDevModelAndDynaPara', dict[str, str|List[str]]) -> str|List[str]|None
        for p_name, record_str in inputs.items():
            kafka_msg = ujson.loads(record_str)
            record = kafka_msg[JsonKey.MESSAGE.value]
            device_infos = record['deviceinfo']  # type: Optional[list]
            single_record = copy.deepcopy(record)
            for device_info in device_infos:
                single_record['deviceinfo'] = [device_info]
                dev_model_key = self.get_device_model_key(device_info)
                dynamic_para_key = self.get_dynamic_para_key(device_info)
                dev_model = self.get_device_model(dev_model_key, device_info[JsonKey.DEVICE_ID.value])
                dynamic_para = self.get_dynamic_para(dynamic_para_key)
                if not dev_model:
                    import time
                    exception_info = "%s:未找到模型%s，请检查模型是否注册" % (
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), dynamic_para_key)
                    single_record['exceptions'] = [exception_info]
                if dynamic_para:
                    single_record['dynamicpara'] = dynamic_para
                else:
                    single_record['dynamicpara'] = {}
                single_record['nodes'] = dev_model['nodes']
                single_record['edges'] = dev_model['edges']
                single_record['datasource'] = [[]]
                # logger.info("kafka_msg type:%a" % type(kafka_msg))
                kafka_msg[JsonKey.MESSAGE.value] = single_record
                yield ujson.dumps(kafka_msg)

    def get_device_model(self, row_key, did):
        """
        根据 row_key 获取 redis 缓存
        :param row_key: row key
        :param did: id
        :return: device model dict
        """
        device_model = self.redis_manager.get(row_key)
        return ujson.loads(device_model) if utils.is_not_blank(device_model) \
            else {
            "assetid": did,
            "dataUpdateTime": None,
            "nodes": [],
            "edges": []
        }

    def get_dynamic_para(self, row_key):
        """
        根据 row_key 获取 redis 缓存
        :param row_key: row key
        :return: dynamic para dict
        """
        dynamic_para = self.redis_manager.get(row_key)
        return ujson.loads(dynamic_para) if utils.is_not_blank(dynamic_para) \
            else {}

    @staticmethod
    def get_device_model_key(device_info):
        # type: (dict[str, str]) -> str
        if JsonKey.DEVICE_ID.value not in device_info:
            raise error.TransformError("redis row key, %s not found: %s"
                                       % (JsonKey.DEVICE_ID.value, ujson.dumps(device_info)))
        return "{DevModel}:%s" % (device_info[JsonKey.DEVICE_ID.value])

    # noinspection SpellCheckingInspection
    @staticmethod
    def get_dynamic_para_key(device_info):
        # type: (dict[str, str]) -> str
        if JsonKey.DEVICE_ID.value not in device_info:
            raise error.TransformError("redis row key, %s not found: %s"
                                       % (JsonKey.DEVICE_ID.value, ujson.dumps(device_info)))
        return "{dynamicpara}:%s" % (device_info[JsonKey.DEVICE_ID.value])


class RuleSaveRedisBuffer(RayTransform):

    def __init__(self,  # type: RuleSaveRedisBuffer
                 key_prefix=None,  # type: str
                 options=None,  # type: Optional[PipelineOptions]
                 parallel=None,  # type: Optional[int]
                 num_cpus=0.5,  # type: float
                 num_gpus=0,  # type: float
                 worker_index=-1,  # type: int
                 ):
        # type: (...) -> None
        super().__init__(worker_index,
                         parallel=parallel,
                         num_cpus=num_cpus,
                         num_gpus=num_gpus,
                         options=options)
        self.key_prefix = key_prefix
        self._redis_manager = None  # type: Optional[RedisManager]

    def pre_startup(self):
        super().pre_startup()
        if self.key_prefix is None:
            self.key_prefix = self.options.get_pipeline_namespace()
        logger.info("key_prefix: %s", self.key_prefix)
        self._redis_manager = RedisManager(self.options)

    @property
    def redis_manager(self):
        return self._redis_manager

    async def process(self, inputs):
        # type: ('RuleSaveRedisBuffer', dict[str, str|List[str]]) -> str|List[str]|None
        for name, record_str in inputs.items():
            record = ujson.loads(record_str)
            row_key = get_row_key(self.key_prefix, record)
            value_node = record[JsonKey.MESSAGE.value]  # type: Optional[dict]
            if JsonKey.CACHE.value in value_node:
                record_cache = value_node[JsonKey.CACHE.value]
                self.redis_manager.set(row_key, ujson.dumps(record_cache))
            yield record_str


class RedisUpdateDynaPara(RayTransform):
    def __init__(self,  # type: RedisUpdateDynaPara
                 options=None,  # type: Optional[PipelineOptions]
                 parallel=None,  # type: Optional[int]
                 num_cpus=0.5,  # type: float
                 num_gpus=0,  # type: float
                 worker_index=-1,  # type: int
                 ):
        # type: (...) -> None
        super().__init__(worker_index,
                         parallel=parallel,
                         num_cpus=num_cpus,
                         num_gpus=num_gpus,
                         options=options)
        self._redis_manager = None  # type: Optional[RedisManager]

    def pre_startup(self):
        super().pre_startup()
        self._redis_manager = RedisManager(self.options)

    @property
    def redis_manager(self):
        return self._redis_manager

    async def process(self, inputs):
        # type: ('RedisUpdateDynaPara', dict[str, str|List[str]]) -> str|List[str]|None
        for p_name, record_str in inputs.items():
            kafka_msg = ujson.loads(record_str)
            record = kafka_msg[JsonKey.MESSAGE.value]
            if record and record.get('key') and record.get('value'):
                update_value = record.get('value')
                dynamic_para_key = self.get_dynamic_para_key(record)
                dynamic_para_value = self.get_dynamic_para(dynamic_para_key)  # type:dict
                # 更新参数
                dynamic_para_value.update(update_value)
                self.redis_manager.set(dynamic_para_key, ujson.dumps(dynamic_para_value))
                yield record_str

    # noinspection SpellCheckingInspection
    @staticmethod
    def get_dynamic_para_key(record):
        # type: (dict[str, object]) -> str
        if JsonKey.KEY.value not in record:
            raise error.TransformError("kafka row key, %s not found: %s"
                                       % (JsonKey.KEY.value, ujson.dumps(record)))
        return "{dynamicpara}:%s" % (record[JsonKey.KEY.value])

    def get_dynamic_para(self, row_key):
        """
        根据 row_key 获取 redis 缓存
        :param row_key: row key
        :return: dynamic para dict
        """
        dynamic_para = self.redis_manager.get(row_key)
        return ujson.loads(dynamic_para) if utils.is_not_blank(dynamic_para) \
            else {}


# noinspection SpellCheckingInspection
class RedisReadDevModel(RayTransform):
    def __init__(self,  # type: RedisReadDevModel
                 options=None,  # type: Optional[PipelineOptions]
                 parallel=None,  # type: Optional[int]
                 num_cpus=0.5,  # type: float
                 num_gpus=0,  # type: float
                 worker_index=-1,  # type: int
                 ):
        super().__init__(worker_index,
                         parallel=parallel,
                         num_cpus=num_cpus,
                         num_gpus=num_gpus,
                         options=options)
        self._redis_manager = None  # type: Optional[RedisManager]

    def pre_startup(self):
        super().pre_startup()
        self._redis_manager = RedisManager(self.options)

    @property
    def redis_manager(self):
        return self._redis_manager

    async def process(self, inputs):
        # type: ('RedisReadDevModel', dict[str, str|List[str]]) -> str|List[str]|None
        for p_name, record_str in inputs.items():
            record = ujson.loads(record_str)
            model = self.get_redis_model('{DevModel}:' + record[JsonKey.ID.value])
            exceptions = []
            device_model: DeviceModel
            if utils.is_not_blank(model):
                device_model = DataUtils.convert_keys_to_lowercase(ujson.loads(model))
                if 'metamodel' not in device_model or len(device_model['metamodel']) == 0:
                    device_model['metamodel'] = {}
            else:
                now = datetime.now()
                formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
                exception: ExceptionExe = {'exception': "未找到模型，请检查模型是否注册",
                                           'exceptiontype': "no model",
                                           'issuer': "RedisReadDevModel",
                                           'time': formatted_now,
                                           'group': "Critical",
                                           'inputjson': "",
                                           'runningtime': ""
                                           }
                exceptions.append(exception)
                device_model = {'nodes': [], 'edges': [], 'metamodel': {}}
            graph: Graph = GraphUtils.get_graph(record)
            graph['nodes'] = device_model['nodes']
            graph['edges'] = device_model['edges']
            graph['metamodel'] = device_model['metamodel']
            graph['version'] = "1.0.0"
            graph['exceptions'] = exceptions
            graph['warnings'] = {}
            record['_message'] = graph
            yield ujson.dumps(record, ensure_ascii=False)

    def get_redis_model(self, row_key):
        """
        根据 row_key 获取 redis model
        :param row_key: row key
        :return: model DevModel
        """
        return self.redis_manager.get(row_key)


def get_row_key(key_prefix, record):
    # type: (str, dict[str, str]) -> str
    if JsonKey.ID.value not in record:
        raise error.TransformError("redis row key, %s not found: %s"
                                   % (JsonKey.ID.value, ujson.dumps(record)))
    return "{%s}:%s" % (key_prefix, record[JsonKey.ID.value])

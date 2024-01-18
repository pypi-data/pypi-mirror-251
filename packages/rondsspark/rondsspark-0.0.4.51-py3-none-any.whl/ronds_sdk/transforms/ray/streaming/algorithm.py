import asyncio
import datetime
import traceback
from typing import List, Optional, Dict

import ujson

from ronds_sdk import logger_config, PipelineOptions
from ronds_sdk.dataframe.window import WindowDF, WindowSortedList
from ronds_sdk.datasources.cassandra_manager import CassandraManager
from ronds_sdk.datasources.redis_manager import RedisManager
from ronds_sdk.models.graph import Cache, ExceptionExe
from ronds_sdk.models.message import Message
from ronds_sdk.options.pipeline_options import AlgorithmOptions, RedisOptions, CassandraOptions
from ronds_sdk.parser.rule_parser import EditorRuleParser
from ronds_sdk.tools import utils
from ronds_sdk.tools.buffer_utils import BufferUtils
from ronds_sdk.tools.constants import JsonKey
from ronds_sdk.tools.exception_utils import ExceptionUtils
from ronds_sdk.tools.json_utils import JsonUtils
from ronds_sdk.transforms import ronds
from ronds_sdk.transforms.pandas.rule_merge_data import RuleData
from ronds_sdk.transforms.pandas.transforms import Algorithm
from ronds_sdk.transforms.ray.base import RayTransform

logger = logger_config.config()


class RuleWindowAlgorithm(RayTransform):
    """
    algorithm call with window buffer for rule editor
    """

    def __init__(self,  # type: RuleWindowAlgorithm
                 rules,  # type: list[dict] # 规则集合
                 dt_column,  # type: str  # 时间字段
                 options=None,  # type: Optional[PipelineOptions]
                 id_column="id",  # type: str
                 measure_column="Value",  # type: str
                 parallel=None,  # type: int
                 worker_index=-1,  # type: int
                 ):
        super().__init__(worker_index, parallel=parallel, options=options)
        self.rules = rules
        self.dt_column = dt_column
        self._id_column = id_column
        self._measure_column = measure_column
        self.rule_groups = set()
        self.algorithm = None  # type: Optional[Algorithm]
        self.window_buffer = None  # type: Optional[WindowSortedList]

    def pre_startup(self):
        super().pre_startup()
        alg_options = self.options.view_as(AlgorithmOptions)
        self.algorithm = Algorithm(
            ronds.Algorithm(alg_options.alg_path(), alg_options.alg_func()),
            self.options)
        self.window_buffer = WindowSortedList(alg_options.window_duration(),
                                              alg_options.window_slide_duration(),
                                              self._time_key)

    def _time_key(self, record) -> 'datetime.datetime':
        try:
            return datetime.datetime.strptime(record.get(self.dt_column), utils.datetime_format())
        except Exception as ex:
            logger.error("_time_key format failed, return now() instead: %s, %s",
                         ex, traceback.format_exc())
            return datetime.datetime.now()

    async def consume(self):
        """
        从上游消费最新数据, 缓存到本地 buffer
        :return: 常驻任务, 不结束, 无返回值
        """
        while True:
            try:
                current_dict = await self.fetch_currents(no_wait=True)
                if utils.collection_empty(current_dict):
                    await asyncio.sleep(1)
                    continue
                for _, message_str in current_dict.items():
                    message = JsonUtils.loads(message_str)
                    record = message[JsonKey.MESSAGE.value]
                    rule_group = message[JsonKey.RULE_GROUP.value]
                    aid = record[self._id_column]
                    if rule_group is None or aid is None:
                        await asyncio.sleep(0)
                        continue
                    self.rule_groups.add(rule_group)
                    self.window_buffer.append(record, partition=aid)
                    if self.window_buffer.should_schedule(record):
                        query_res = self.window_buffer.query()
                        await self.alg_process(query_res)
                self.success()
            except Exception as ex:
                self.failed(e=ex)
                await asyncio.sleep(0)

    async def alg_process(self, df_dict):
        if utils.collection_empty(df_dict):
            return
        for rule_group in self.rule_groups:
            rule = self.rules[rule_group]
            device_id = rule.get(JsonKey.ASSET_ID.value)
            rule_id_list = EditorRuleParser.rule_ids(rule)
            point_id_list = EditorRuleParser.point_ids(rule)
            rule_data = RuleData(device_id, rule_id_list, desc=False)
            self._rule_data_process(rule_data, point_id_list, df_dict)
            alg_res = self._alg_call(rule_data)
            record = {
                JsonKey.ID.value: device_id,
                JsonKey.MESSAGE.value: alg_res
            }
            await self.send(ujson.dumps(record))

    def _rule_data_process(self,
                           rule_data: 'RuleData',
                           point_id_list: "List",
                           df_dict: Dict[str, List[Dict]]
                           ):
        for point_id in point_id_list:
            if point_id not in df_dict:
                continue
            rows = df_dict[point_id]
            s_date = None
            for row in rows:
                dt = self._time_key(row).strftime(utils.datetime_format())
                if s_date is None:
                    s_date = dt
                rule_data.add_process_data(point_id, dt, row.get(self._measure_column))
            rule_data.set_datasourcetimes([s_date])

    def _alg_call(self, rule_data):
        # type: ('RuleWindowAlgorithm', RuleData) -> dict
        data_dict = rule_data.get_data()
        alg_dict = self.algorithm.algorithm_call(data_dict)
        return alg_dict


class RuleBaseAlgorithm(RayTransform):

    def __init__(self,  # type: RuleBaseAlgorithm
                 graph_config,  # type: str # 算法配置
                 options=None,  # type: Optional[PipelineOptions]
                 parallel=None,  # type: int
                 num_cpus=0.5,  # type: float
                 num_gpus=0,  # type: float
                 worker_index=-1,  # type: int
                 is_merge=False,  # type: bool
                 ):
        super().__init__(worker_index,
                         parallel=parallel,
                         num_cpus=num_cpus,
                         num_gpus=num_gpus,
                         options=options,
                         is_merge=is_merge)
        self.graph_config = graph_config
        self.algorithm = None  # type: Optional[Algorithm]
        self.window_buffer = None  # type: Optional[WindowDF]

    def pre_startup(self):
        super().pre_startup()
        alg_options = self.options.view_as(AlgorithmOptions)
        self.algorithm = Algorithm(
            ronds.Algorithm(alg_options.alg_path(), alg_options.alg_func()),
            self.options)

    async def process(self, inputs):
        # type: ('RuleBaseAlgorithm', dict[str, str | List[str]]) -> str | List[str] | None
        for p_name, record_str in inputs.items():
            record = ujson.loads(record_str)
            graph_transforms(self.graph_config, record)
            try:
                alg_res = self.algorithm.algorithm_call(record[JsonKey.MESSAGE.value])
                record[JsonKey.MESSAGE.value] = alg_res
                yield JsonUtils.dumps(record)
            except Exception as ex:
                record = ujson.loads(record_str)
                exception = (ExceptionUtils
                             .get_exception(str(ex) + traceback.format_exc(),
                                            "algorithm call failed", "RuleBaseAlgorithm",
                                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                            "Critical", "", ""))
                record['_message']['exceptions'] = [exception]
                yield JsonUtils.dumps(record)


class RuleBaseAlgorithmWithBuffer(RayTransform):

    def __init__(self,  # type: RuleBaseAlgorithmWithBuffer
                 graph_config,  # type: str # 算法配置
                 buffer_sources=None,  # type: dict # buffer配置
                 options=None,  # type: Optional[PipelineOptions]
                 parallel=None,  # type: int
                 num_cpus=0.5,  # type: float
                 num_gpus=0,  # type: float
                 worker_index=-1,  # type: int
                 is_merge=False,  # type: bool
                 ):
        super().__init__(worker_index,
                         parallel=parallel,
                         num_cpus=num_cpus,
                         num_gpus=num_gpus,
                         options=options,
                         is_merge=is_merge)
        self.buffer_id = None
        self.buffer_sources = buffer_sources
        self.redis_options = None
        self.cassandra_options = None
        self.graph_config = graph_config
        self.buffer_sources = buffer_sources
        self.algorithm = None  # type: Optional[Algorithm]
        self.window_buffer = None  # type: Optional[WindowDF]
        self._redis_manager = None  # type: Optional[RedisManager]
        self._cassandra_manager = None  # type: Optional[CassandraManager]

    def pre_startup(self):
        super().pre_startup()
        read_buffer = self.buffer_sources[JsonKey.READ_RULE_ALGORITHM_BUFFER.v]
        if 'customWorkflowId' in read_buffer and read_buffer['customWorkflowId'] is not None:
            self.buffer_id = read_buffer['customWorkflowId']
        else:
            self.buffer_id = self.options.get_pipeline_namespace()
        redis_options = self.options.view_as(RedisOptions)
        self._redis_manager = RedisManager(redis_options)
        cassandra_options = self.options.view_as(CassandraOptions)
        self._cassandra_manager = CassandraManager(cassandra_options)
        alg_options = self.options.view_as(AlgorithmOptions)
        self.algorithm = Algorithm(
            ronds.Algorithm(alg_options.alg_path(), alg_options.alg_func()),
            alg_options)

    async def process(self, inputs):
        # type: ('RuleBaseAlgorithmWithBuffer', dict[str, str | List[str]]) -> str | List[str] | None
        read_cassandra_source = self.buffer_sources[JsonKey.READ_RULE_ALGORITHM_BUFFER.v]['cassandraSource']
        # noinspection SpellCheckingInspection
        is_read_cassandra = (read_cassandra_source is not None and
                             read_cassandra_source['keyspace'] is not None and
                             read_cassandra_source['dtnames'] is not None)
        for _, record_str in inputs.items():
            record: Message = ujson.loads(record_str)
            if is_read_cassandra:
                try:
                    cache: Cache = BufferUtils.get_redis_cassandra_buffer(self.buffer_id, record['id'],
                                                                          self._redis_manager, self._cassandra_manager)
                    graph_transforms(self.graph_config, record, cache)
                except Exception as ex:
                    mount_exception_to_graph(record, ex)
                    graph_transforms(self.graph_config, record)
            else:
                BufferUtils.get_redis_buffer(self.buffer_id, record['id'], self._redis_manager)
            try:
                alg_res = self.algorithm.algorithm_call(record['_message'])
                write_alg_buffer(self.buffer_id, alg_res, self._redis_manager)
                record['_message'] = alg_res
                yield JsonUtils.dumps(record)
            except Exception as ex:
                record = ujson.loads(record_str)
                exception = (ExceptionUtils
                             .get_exception(str(ex) + traceback.format_exc(),
                                            "algorithm call failed", "RuleBaseAlgorithmWithBuffer",
                                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                            "Critical", "", ""))
                record['_message']['exceptions'] = [exception]
                yield JsonUtils.dumps(record)


def graph_transforms(graph_config, record, cache: Cache = None):
    alg_record = record['_message']
    if 'deviceid' not in alg_record:
        alg_record[JsonKey.DEVICE_ID.v] = record['id']
    if graph_config is not None:
        alg_record[JsonKey.GRAPH_CONFIG.v] = graph_config
    if 'metamodel' not in alg_record:
        alg_record['metamodel'] = {}
    if 'userdata' not in alg_record:
        alg_record['userdata'] = []
    if cache is not None:
        alg_record['cache'] = cache


def mount_exception_to_graph(record, ex):
    alg_record = record['_message']
    # noinspection SpellCheckingInspection
    exception: ExceptionExe = {'exception': str(ex),
                               'exceptiontype': "Get device buffer and merge graph error",
                               'issuer': "Executor",
                               'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                               'group': "Critical",
                               'inputjson': "",
                               'runningtime': ""
                               }
    exceptions = [exception]
    alg_record['exceptions'] = exceptions
    alg_record['cache'] = {'deviceid': record['id'], 'metadata': [], 'buffer': ''}


def write_alg_buffer(buffer_id, row, redis_manager: RedisManager):
    if not ('exceptions' in row and len(row['exceptions']) > 0):
        BufferUtils.write_redis_buffer(buffer_id, row['cache'], redis_manager)
    row['cache']['buffer'] = ''
    row['cache']['metadata'] = []

from datetime import datetime
from typing import Optional, List
import ujson

from ronds_sdk.models.graph import ExceptionExe, Graph
from ronds_sdk.models.message import Message
from ronds_sdk import PipelineOptions, logger_config
from ronds_sdk.datasources.http_manager import HttpManager
from ronds_sdk.tools.constants import JsonKey
from ronds_sdk.tools.data_utils import DataUtils
from ronds_sdk.tools.graph_utils import GraphUtils
from ronds_sdk.transforms.ray.base import RayTransform

logger = logger_config.config()


class HttpGetDevModel(RayTransform):
    def __init__(self,  # type: HttpGetDevModel
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
        self._http_manager = None  # type: Optional[HttpManager]

    def pre_startup(self):
        super().pre_startup()
        self._http_manager = HttpManager(self.options)

    @property
    def http_manager(self):
        return self._http_manager

    # noinspection SpellCheckingInspection
    async def process(self, inputs):
        # type: ('HttpGetDevModel', dict[str, str|List[str]]) -> str|List[str]|None
        device_ids = self.get_device_ids(inputs)
        exceptions = []
        device_model_dict = {}
        try:
            # from ronds_sdk.tools import utils
            # utils.break_point()
            device_models = await self._http_manager.async_call_post_api(device_ids)
            device_model_list = ujson.loads(device_models)['data']
            if device_model_list is None:
                now = datetime.now()
                formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
                exception: ExceptionExe = {'exception': "Call device model http status is not 200",
                                           'exceptiontype': "ERROR:read device model ",
                                           'issuer': "HttpGetDevModel",
                                           'time': formatted_now,
                                           'group': "Critical",
                                           'inputjson': "",
                                           'runningtime': ""
                                           }
                exceptions.append(exception)
            else:
                for item in device_model_list:
                    device_model_dict[item['assetid']] = item['nodeedges']
        except Exception as ex:
            now = datetime.now()
            formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
            exception: ExceptionExe = {
                'exception': str(ex),
                'exceptiontype': "ERROR:get device model failed",
                'issuer': "HttpGetDevModel",
                'time': formatted_now,
                'group': "Critical",
                'inputjson': "",
                'runningtime': ""
            }
            exceptions.append(exception)
        for p_name, record_str in inputs.items():
            record: Message = ujson.loads(record_str)
            graph: Graph = GraphUtils.get_graph(record)
            graph['version'] = "1.0.0"
            graph['warnings'] = {}
            graph['exceptions'] = exceptions
            deviceid = graph['cache']['deviceid']
            if deviceid in device_model_dict:
                device_model = device_model_dict[deviceid]
                graph['nodes'] = DataUtils.convert_keys_to_lowercase(device_model['nodes'])
                graph['edges'] = DataUtils.convert_keys_to_lowercase(device_model['edges'])
            else:
                graph['nodes'] = []
                graph['edges'] = []
            record['_message'] = graph
            yield ujson.dumps(record, ensure_ascii=False)

    @staticmethod
    def get_device_ids(inputs) -> str:
        """
        获取设备id集合
        """
        device_ids = []
        for name, record_str in inputs.items():
            record = ujson.loads(record_str)
            device_id = record[JsonKey.ID.value]
            device_ids.append(device_id)
        return ujson.dumps(device_ids)

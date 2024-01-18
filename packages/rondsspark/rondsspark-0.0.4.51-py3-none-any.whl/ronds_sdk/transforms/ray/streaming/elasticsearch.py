import datetime
import uuid

import pytz
import ujson
from typing import List, Optional

from ronds_sdk import logger_config
from ronds_sdk.datasources.es_manager import ESManager
from ronds_sdk.models.exception_info import ExceptionCategory, ExceptionSource, ExceptionInfo
from ronds_sdk.options.pipeline_options import ESOptions
from ronds_sdk.tools.constants import JsonKey
from ronds_sdk.transforms.ray.base import RayTransform

logger = logger_config.config()


class ESSaveAlgException(RayTransform):
    def __init__(self,  # type: ESSaveAlgException
                 options=None,  # type: Optional[ESOptions]
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
        self.index_name = options.get_index()  # type: Optional[dict]
        self.es_source = None  # type: Optional[ESManager]
        self.options = options

    def pre_startup(self):
        super().pre_startup()
        if not self.es_source:
            self.es_source = ESManager(self.options)
        if self.options.get_index_auto_create():
            self.es_source.create_index(self.options.get_index(), self.options.get_mapping())

    # noinspection SpellCheckingInspection
    async def process(self, inputs):
        # type: ('ESSaveAlgException', dict[str, str|List[str]]) -> str|List[str]|None
        for p_name, records_str in inputs.items():
            from ronds_sdk.tools import utils
            utils.break_point()
            kafka_msg = ujson.loads(records_str)
            record = kafka_msg[JsonKey.MESSAGE.value]
            if record.get('exceptions', None):
                for exception_obj in record['exceptions']:
                    if exception_obj.get('exceptiontype', None) and exception_obj.get('time', None):
                        source = self._get_exception_source(kafka_msg)
                        exception_info = self._get_exception_info(record_id=uuid.uuid4(),
                                                                  workflowid=record.get('workflowid', None),
                                                                  category=ExceptionCategory.EXCEPTION,
                                                                  exception_type=exception_obj.get('exceptiontype', None),
                                                                  group=exception_obj.get('group', None),
                                                                  total=1,
                                                                  message=exception_obj.get('exceptiontype', None),
                                                                  stack=exception_obj.get('exception', None),
                                                                  source=source,
                                                                  create_time=exception_obj.get('time', None),
                                                                  creator=exception_obj.get('issuer', None))
                        await self.es_source.add_data(self.index_name, exception_info)
            warnings = record.get('warnings', None)
            if warnings:
                for k, v in warnings.items():
                    source = self._get_exception_source(kafka_msg)
                    exception_info = self._get_exception_info(record_id=uuid.uuid4(),
                                                              workflowid=record.get('workflowid', None),
                                                              category=ExceptionCategory.WARNING,
                                                              exception_type=k,
                                                              group=v.get('group', None),
                                                              total=v.get('count', None),
                                                              message=v.get('detail', None),
                                                              stack='',
                                                              source=source,
                                                              create_time=v.get('time', None),
                                                              creator=v.get('issuer', None),)
                    await self.es_source.add_data(self.index_name, exception_info)
        yield records_str

    @staticmethod
    def _get_exception_source(kafka_msg):
        source = ExceptionSource()
        source['topic'] = kafka_msg['topic']
        source['partition'] = kafka_msg['partition']
        source['offset'] = kafka_msg['offset']
        return source

    @staticmethod
    def _get_exception_info(
                            record_id,  # type: str
                            workflowid,  # type: str
                            category,  # type: str
                            exception_type,  # type: str
                            group,  # type: str
                            total,  # type: int
                            message,  # type: str
                            stack,  # type: str
                            source,  # type: str
                            create_time,  # type: str
                            creator,  # type: str
                            ):
        exception_info = ExceptionInfo()
        exception_info['record_id'] = record_id
        exception_info['workflowid'] = workflowid
        exception_info['category'] = category
        exception_info['exception_type'] = exception_type
        exception_info['group'] = group
        exception_info['total'] = total
        exception_info['message'] = message
        exception_info['stack'] = stack
        # 解析时间字符串为 datetime 对象（假设时间字符串已经是 UTC 时间）
        datetime_obj = datetime.datetime.strptime(create_time, "%Y-%m-%d %H:%M:%S.%f")
        datetime_obj = datetime_obj.astimezone(datetime.timezone.utc)
        datetime_obj_str = datetime_obj.strftime("%Y-%m-%dT%H:%M:%S.%f")
        exception_info['create_time'] = datetime_obj_str
        exception_info['creator'] = creator
        exception_info['source'] = ujson.dumps(source)
        return exception_info

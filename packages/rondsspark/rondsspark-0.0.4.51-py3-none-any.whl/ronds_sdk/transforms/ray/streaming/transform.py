import traceback
from datetime import datetime

import ujson
from typing import List

from ronds_sdk.models.message import Message
from ronds_sdk.tools.exception_utils import ExceptionUtils
from ronds_sdk.tools.json_utils import JsonUtils
from ronds_sdk.transforms.ray.base import RayTransform


class GraphTransform(RayTransform):
    def __init__(self,  # type: GraphTransform
                 parallel=None,  # type: int
                 num_cpus=0.5,  # type: float
                 num_gpus=0,  # type: float
                 worker_index=-1,  # type: int
                 ):
        # type: (...) -> None
        super().__init__(worker_index,
                         parallel=parallel,
                         num_cpus=num_cpus,
                         num_gpus=num_gpus)

    def pre_startup(self):
        super().pre_startup()

    async def process(self, inputs):
        # type: ('GraphTransform', dict[str, str|List[str]]) -> str|List[str]|None
        for _, record_str in inputs.items():
            record: Message = ujson.loads(record_str)
            try:
                record_message = record['_message']
                traceinfos: List = record_message['traceinfos']
                traceinfos.append({'site': record['topic'], 'arrivetimes': [record['arrive_time']]})
                yield JsonUtils.dumps(record)
            except Exception as ex:
                exception = (ExceptionUtils
                             .get_exception(str(ex) + traceback.format_exc(),
                                            "graph transform failed", "GraphTransform",
                                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                            "Critical", "", ""))
                record['_message']['exceptions'] = [exception]
                yield JsonUtils.dumps(record)

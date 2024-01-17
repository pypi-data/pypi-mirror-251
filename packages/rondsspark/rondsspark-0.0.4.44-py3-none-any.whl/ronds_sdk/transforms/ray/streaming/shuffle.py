import asyncio
from typing import TYPE_CHECKING, List

import ujson

from ronds_sdk import logger_config, error
from ronds_sdk.tools import utils
from ronds_sdk.tools.constants import ExpandChainType
from ronds_sdk.tools.shuffle import json_hash_partitioner
from ronds_sdk.transforms.ray.base import RayTransform

if TYPE_CHECKING:
    from typing import Callable

logger = logger_config.config()


class Shuffle(RayTransform):

    def __init__(self,  # type: Shuffle
                 shuffle_key=None,  # type: str,
                 partitioner=json_hash_partitioner,  # type: Callable
                 parallel=None,  # type: int
                 num_cpus=0.5,  # type: float
                 num_gpus=0,  # type: float
                 worker_index=-1,  # type: int
                 ):
        # type: (...) -> None
        super().__init__(worker_index, parallel=parallel, num_cpus=num_cpus,
                         num_gpus=num_gpus, is_merge=True)
        self._expand_chain_type = ExpandChainType.ONE_TO_ALL
        self.partitioner = partitioner  # type: Callable
        self.shuffle_key = shuffle_key
        self.shuffle_num = self.parallel

    async def consume(self):
        logger.info("%s: receiver size: %d, %s", str(self), len(self.downstream()), self.downstream())
        while True:
            current_dict = await self.fetch_currents()
            if utils.collection_empty(current_dict):
                await asyncio.sleep(1)
                continue
            for input_name, json_str in current_dict.items():
                part_dict = self.partitioner(json_str, self.shuffle_key)
                await self.send(part_dict)

    async def send(self,
                   part_dict,  # type: dict[int, List[str]]
                   ):
        # send remote records
        for hash_key, items in part_dict.items():
            for _, receivers_instances in self.downstream().items():
                await self.shuffle_send(receivers_instances, hash_key, items)

    async def shuffle_send(self, receivers_instances, hash_key, items):
        parallel = len(receivers_instances)
        worker_index = hash_key % parallel
        if receivers_instances[worker_index] is None:
            raise error.TransformError("parallel=%d, worker_index=%d lost!"
                                       % (parallel, worker_index))
        for item in items:
            logger.debug("worker_index: %d, send item: %s" % (worker_index, ujson.dumps(item)))
            await receivers_instances[worker_index].receive(self.consumer_id, item)

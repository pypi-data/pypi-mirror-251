import json
import os

import ray
from ray.actor import ActorClass
from ray.remote_function import RemoteFunction

from ronds_sdk import error, logger_config
from ronds_sdk.tools import utils
from ronds_sdk.transforms.ray.base import RayTransform
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from typing import Callable, List

logger = logger_config.config()


def json_hash_partitioner(json_str, shuffle_key, shuffle_num, input_name):
    # type: (str, str, int, str) -> dict[int, List[str]]
    json_obj = json.loads(json_str)
    res_dict = dict()
    if isinstance(json_obj, list):
        for json_dict in json_obj:
            assert isinstance(json_dict, dict)
            hash_key = utils.dict_hash_mod(json_dict, shuffle_key, shuffle_num)
            dict_put(res_dict, hash_key, json.dumps(json_dict))
    else:
        hash_key = utils.dict_hash_mod(json_obj, shuffle_key, shuffle_num)
        dict_put(res_dict, hash_key, json_str)
    return res_dict


def dict_put(m_dict, key, value):
    # type: (dict, int, str) -> None
    if not m_dict.__contains__(key):
        m_dict[key] = list()
    m_dict[key].append(value)


class Shuffle(RayTransform):

    def __init__(self,  # type: Shuffle
                 shuffle_key=None,  # type: str,
                 partitioner=json_hash_partitioner,  # type: Callable
                 parallel=None,  # type: int
                 worker_index=-1,  # type: int
                 ):
        # type: (...) -> None
        super().__init__(worker_index, parallel=parallel)
        self.partitioner = partitioner  # type: Callable
        self.shuffle_key = shuffle_key
        self.shuffle_num = self.parallel
        # noinspection PyTypeChecker
        self.receiver = None  # type: list[Union[RemoteFunction, ActorClass]]

    def set_receiver(self, receivers):
        # type: (list[Union[RemoteFunction, ActorClass]]) -> None
        self.receiver = receivers

    async def consume(self):
        while True:
            current_dict = await self.fetch_currents()
            for input_name, json_str in current_dict.items():
                part_dict = self.partitioner(json_str, self.shuffle_key, self.shuffle_num, input_name)
                await self.send(part_dict)

    async def send(self,
                   part_dict,  # type: dict[int, List[str]]
                   ):
        # records put local buffer first, avoid remote call
        if part_dict.__contains__(self.worker_index):
            await self.receive(part_dict.get(self.worker_index))
        logger.debug("send, pid: %s" % os.getpid())
        # send remote records
        for worker_index, items in part_dict.items():
            if self.worker_index == worker_index:
                continue
            if worker_index >= len(self.receiver):
                raise error.TransformError('lost shuffle task, worker_index: %d' % worker_index)
            await self.receiver[worker_index].receive.remote(items)

    async def receive(self, items):
        for item in items:
            await self.buffer.put(item)

    def deploy(self, upstreams=None, parallel=None):
        # type: (list[Union[ActorClass, RemoteFunction]], int) -> list[Union[ActorClass, RemoteFunction]]
        shuffle_list = super().deploy(upstreams, parallel)
        wait_list = list()

        # set shuffle
        for shuffle in shuffle_list:
            wait_list.append(shuffle.set_receiver.remote(shuffle_list))
        ray.get(wait_list)
        return shuffle_list

import traceback
from asyncio import Queue, QueueEmpty
from typing import List

from ronds_sdk import logger_config

logger = logger_config.config()


class MultiKeyBuffer(object):
    def __init__(self, maxsize, keys=None):
        # type: (int, List[str]) -> None
        self.key_queue = dict()  # type: dict[str, Queue]
        self.maxsize = maxsize
        if keys is not None:
            for key in keys:
                self.key_queue[key] = Queue(maxsize=maxsize)

    def items(self):
        return self.key_queue.items()

    async def key_put(self, key, value):
        try:
            if value is not None:
                await self.key_queue.setdefault(key, Queue(maxsize=self.maxsize)).put(value)
        except Exception as ex:
            logger.error("MultiKeyBuffer put [%s - %s] failed, %s: %s"
                         % (key, value, type(ex), traceback.format_stack()))

    async def put(self, value):
        if value is None or value == '':
            return
        for key in self.key_queue.keys():
            await self.key_put(key, value)

    # noinspection PyBroadException
    async def key_get(self, key, no_wait=False):
        try:
            if no_wait:
                try:
                    return self.key_queue.setdefault(key, Queue(maxsize=self.maxsize)).get_nowait()
                except QueueEmpty:
                    return None
            else:
                return await self.key_queue.setdefault(key, Queue(maxsize=self.maxsize)).get()
        except Exception as ex:
            logger.error("MultiKeyBuffer get [%s] failed, %s: %s"
                         % (key, type(ex), traceback.format_stack()))
            return None

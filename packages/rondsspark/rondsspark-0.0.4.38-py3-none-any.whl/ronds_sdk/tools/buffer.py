import logging
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

    def is_empty(self, key: str) -> bool:
        if not self.key_queue.__contains__(key):
            self.key_queue[key] = Queue(maxsize=self.maxsize)
            return True
        return self.key_queue[key].empty()

    async def key_put(self, key, value):
        if not self.key_queue.__contains__(key):
            self.key_queue[key] = Queue(maxsize=self.maxsize)
        try:
            await self.key_queue[key].put(value)
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
                    return self.key_queue[key].get_nowait()
                except QueueEmpty:
                    return None
            else:
                return await self.key_queue[key].get()
        except Exception as ex:
            logger.error("MultiKeyBuffer get [%s] failed, %s: %s"
                         % (key, type(ex), traceback.format_stack()))
            return None

    async def pop(self, key, no_wait=False, fetch_size=1):
        if not self.key_queue.__contains__(key):
            self.key_queue[key] = Queue(maxsize=self.maxsize)
        if fetch_size == 1:
            return await self.key_get(key, no_wait)
        else:
            m_list = list()
            i = 0
            while i < fetch_size:
                i += 1
                m_list.append(await self.key_get(key, no_wait))
            return m_list

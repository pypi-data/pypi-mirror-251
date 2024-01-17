import traceback
from typing import Optional

import redis
from redis import Redis
from redis.cluster import ClusterNode

from ronds_sdk import PipelineOptions, logger_config
from ronds_sdk.options.pipeline_options import RedisOptions
from ronds_sdk.tools.metaclass import Singleton

logger = logger_config.config()


class RedisManager(metaclass=Singleton):

    def __init__(self, options):
        # type: (PipelineOptions) -> None
        self._redis = None  # type: Optional[Redis]
        self._redis_options = options.view_as(RedisOptions)
        self.expire = self.redis_options.expire_time()
        if self.expire < 0:
            self.expire = None

    @property
    def redis_options(self):
        # type: () -> RedisOptions
        return self._redis_options

    @property
    def redis(self):
        if self._redis is None:
            self._redis = redis.RedisCluster(startup_nodes=[ClusterNode(**node) for node in self.redis_options.nodes()],
                                             username=self.redis_options.username(),
                                             password=self.redis_options.password(),
                                             decode_responses=True)
        return self._redis

    def get(self, key):
        return self.redis.get(key)

    def set(self, key, value, ex=None):
        return self.redis.set(key, value, ex or self.expire)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.redis is not None:
            try:
                self.redis.disconnect_connection_pools()
                logger.info("Redis connection closed")
            except Exception as e:
                logger.error("e: %s, %s" % (e, traceback.format_exc()))

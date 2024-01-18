import unittest

from ronds_sdk import PipelineOptions
from ronds_sdk.datasources.redis_manager import RedisManager


class RedisTest(unittest.TestCase):

    options = PipelineOptions(
        redis_host='172.16.3.221',
        redis_port=7000,
        redis_username='default',
        redis_password='redis123'
    )

    def test_get(self):
        redis_manager = RedisManager(self.options)
        print(redis_manager.get('{a445e7b7-8d3f-4f43-8d0c-057f8f675cfe}:06c86cb1-4479-c2ce-ef1d-c726aa2e7bdb'))

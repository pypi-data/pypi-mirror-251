import uuid
from datetime import datetime

# noinspection PyPackageRequirements
import pytz
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement

from ronds_sdk.datasources.cassandra_manager import CassandraManager
from ronds_sdk.datasources.redis_manager import RedisManager
from ronds_sdk.models.graph import Cache
from ronds_sdk.tools import utils
from ronds_sdk.tools.json_utils import JsonUtils


class BufferUtils(object):
    @staticmethod
    def get_redis_cassandra_buffer(kid, device_id,
                                   redis_manager: RedisManager,
                                   cassandra_manager: CassandraManager) -> Cache:
        redis_buffer = _get_redis_buffer(kid, device_id, redis_manager)
        if utils.is_not_blank(redis_buffer['buffer']):
            return redis_buffer
        else:
            return _get_cassandra_buffer(kid, device_id, cassandra_manager)

    @staticmethod
    def get_redis_buffer(kid, device_id,
                         redis_manager: RedisManager) -> Cache:
        redis_buffer = _get_redis_buffer(kid, device_id, redis_manager)
        return redis_buffer

    @staticmethod
    def write_redis_buffer(kid, cache: Cache, redis_manager: RedisManager):
        _write_redis_buffer(kid, cache, redis_manager)


def _get_redis_buffer(kid, device_id, redis_manager: RedisManager) -> Cache:
    redis_buffer = redis_manager.redis.get("{%s}:%s" % (kid, device_id))
    if utils.is_not_blank(redis_buffer):
        return JsonUtils.loads(redis_buffer)
    else:
        return {'deviceid': device_id, 'buffer': '', 'metadata': []}


def _write_redis_buffer(kid, cache: Cache, redis_manager: RedisManager):
    redis_manager.set("{%s}:%s" % (kid, cache['deviceid']), JsonUtils.dumps(cache))


# noinspection SqlResolve
def _get_cassandra_buffer(kid, device_id, cassandra_manager: CassandraManager) -> Cache:
    sql = (('SELECT workflowid, time, assetid, buffer, metadata FROM {keyspace}.{table} '
           'WHERE workflowid=%s AND time=%s AND assetid=%s')
           .format(keyspace=cassandra_manager.options.get_cassandra_keyspace(),
                   table=cassandra_manager.options.get_cassandra_table_process()))
    params = uuid.UUID(kid), get_buffer_time(), uuid.UUID(device_id)
    result_set = cassandra_manager.query(SimpleStatement(sql, consistency_level=ConsistencyLevel.QUORUM), params)
    cache: Cache = {'deviceid': device_id, 'buffer': '', 'metadata': []}
    if len(result_set.current_rows) > 0:
        for row in result_set:
            cache = {'buffer': row.buffer, 'metadata': JsonUtils.loads(row.metadata)}
    return cache


def get_buffer_time() -> datetime:
    # 获取系统默认时区
    default_timezone = pytz.timezone(
        'UTC' if not hasattr(pytz, 'country_timezones') else pytz.country_timezones['CN'][0])
    buffer_time = datetime(1970, 1, 1, 0, 0, 0, tzinfo=pytz.FixedOffset(480)) \
        if str(default_timezone) == 'Asia/Shanghai' \
        else datetime(1970, 1, 1, 0, 0, 0, tzinfo=pytz.FixedOffset(480))
    return buffer_time

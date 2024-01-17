import datetime
import logging
import uuid
from typing import List, Tuple

from cassandra.cluster import Cluster, Session, ResultSet

from ronds_sdk.models.data import ProcessData, IndexData
from ronds_sdk.options.pipeline_options import CassandraOptions
from ronds_sdk.tools.constants import DEFAULT_RETRY
from ronds_sdk.tools.utils import Singleton, date_format_str

logger = logging.getLogger('executor')
logger.setLevel(logging.INFO)


class CassandraManager(metaclass=Singleton):
    """
    Cassandra 数据库的操作类, 单例
    连接到固定的一个 Cassandra 集群, 可以操作多个 keyspace
    """

    def __init__(self,
                 options,  # type: CassandraOptions
                 ):
        self.cluster = Cluster(options.cassandra_host)
        self.session_cache = dict()  # type: dict[str, Session]

    def get_cache_session(self, keyspace: str, retry=0) -> 'Session':
        if retry > DEFAULT_RETRY:
            raise RuntimeError("cassandra connection failed, retry: %s" % retry)
        if keyspace not in self.session_cache:
            self.session_cache[keyspace] = self.cluster.connect(keyspace)
        session = self.session_cache.get(keyspace)  # type: Session

        if session.is_shutdown:
            self.session_cache.pop(keyspace)
            return self.get_cache_session(keyspace, retry + 1)

        return session

    def query(self, keyspace: str, sql: str, params: List[str]) -> ResultSet:
        result = self.get_cache_session(keyspace).execute(sql, params)
        return result

    def execute(self, keyspace: str, sql: str, params: List[str]) -> None:
        self.get_cache_session(keyspace).execute(sql, params)

    def __del__(self):
        try:
            self.cluster.shutdown()
            logger.info("cassandra cluster shutdown~")
        except Exception as ex:
            logger.error("CassandraManager cluster shutdown failed: %s" % ex)
            raise ex


class QueryManager:
    def window_select(self,
                      uid_list,  # type: List[Tuple[str, int]],
                      start_time,  # type: datetime.datetime
                      end_time,  # type: datetime.datetime
                      ) -> List:
        raise NotImplementedError


class ProcessDataManager(QueryManager, metaclass=Singleton):
    """
    内置的操作工艺数据表
    """

    def __init__(self,
                 options,  # type: CassandraOptions
                 keyspace=None,  # type: str
                 ):
        self._options = options
        self._table_name = options.cassandra_table_process  # type: str
        self.cassandra_manager = CassandraManager(options)  # type: CassandraManager
        if keyspace:
            self.keyspace = keyspace
        elif options.cassandra_keyspace:
            self.keyspace = options.cassandra_keyspace

    def get_cache_session(self):
        return self.cassandra_manager.get_cache_session(self.keyspace)

    # noinspection SqlResolve
    def _get_process_prepare(self, session):
        return session.prepare("""SELECT id, time, value
                                  FROM %s 
                                  where id = ?
                                  AND time >= ? 
                                  AND time < ?""" % self._table_name)

    def window_select(self,
                      uid_list,  # type: List[Tuple[str, int]],
                      start_time,  # type: datetime.datetime
                      end_time,  # type: datetime.datetime
                      ) -> List['ProcessData']:
        try:
            session = self.get_cache_session()
            session_prepare = self._get_process_prepare(session)
            rs_list = []

            for uid, _ in uid_list:
                u_uid = uuid.UUID(uid)
                result_set = session.execute(session_prepare, [u_uid, start_time, end_time])
                for r in result_set:
                    rs_list.append(ProcessData(
                        str(r.id),
                        date_format_str(r.time),
                        r.value
                    ))

            return rs_list
        except Exception as ex:
            logger.error('window_select failed, uid_list: %s, start_time: %s, end_time: %s, ex:\n %s' % (
                str(uid_list), start_time, end_time, str(ex)))
            raise ex


class IndexDataManager(QueryManager, metaclass=Singleton):
    """
    振动特征值查询
    """

    def __init__(self,
                 options,  # type: CassandraOptions
                 keyspace=None,  # type: str
                 ):
        self._options = options
        self._table_name = options.cassandra_table_index  # type: str
        self.cassandra_manager = CassandraManager(options)  # type: CassandraManager
        if keyspace:
            self.keyspace = keyspace
        elif options.cassandra_keyspace:
            self.keyspace = options.cassandra_keyspace

    def get_cache_session(self):
        return self.cassandra_manager.get_cache_session(self.keyspace)

    # noinspection SqlResolve
    def _get_index_prepare(self, session):
        return session.prepare("""SELECT id, datatype, time, value, properties
                                  FROM %s 
                                  where id = ?
                                  AND datatype = ?
                                  AND time >= ? 
                                  AND time < ?""" % self._table_name)

    def window_select(self,
                      uid_list,  # type: List[Tuple[str, int]],
                      start_time,  # type: datetime.datetime
                      end_time,  # type: datetime.datetime
                      ) -> List['IndexData']:
        try:
            session = self.get_cache_session()
            session_prepare = self._get_index_prepare(session)
            rs_list = []

            for uid, data_type in uid_list:
                u_uid = uuid.UUID(uid)
                result_set = session.execute(session_prepare, [u_uid, data_type, start_time, end_time])
                for r in result_set:
                    rs_list.append(IndexData(
                        str(r.id),
                        r.datatype,
                        date_format_str(r.time),
                        r.value,
                        r.properties,
                    ))

            return rs_list
        except Exception as ex:
            logger.error('window_select failed, uid_list: %s, start_time: %s, end_time: %s, ex:\n %s' % (
                str(uid_list), start_time, end_time, str(ex)))
            raise ex

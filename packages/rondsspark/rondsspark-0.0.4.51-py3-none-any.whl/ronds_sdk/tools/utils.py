import datetime
import json
import logging
from typing import Callable, List, Union, Sequence, Optional, Dict, Set

from ronds_sdk import logger_config

logger_config.config()
logger = logging.getLogger('executor')


class WrapperFunc(object):
    def call(self, *args, **kwargs):
        raise NotImplementedError


class ForeachBatchFunc(WrapperFunc):
    def __init__(self,
                 func,  # type: Callable
                 **kwargs
                 ):
        self._func = func
        self._kwargs = kwargs

    def call(self, *args, **kwargs):
        new_kwargs = {**self._kwargs, **kwargs}
        self._func(*args, **new_kwargs)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class RuleParser(object):

    def __init__(self,
                 rule_path,  # type: str
                 ):
        """
        从文件解析 phm 规则编辑器传入的规则配置信息, 用于从 Cassandra 根据指定规则读取测点数据;

        包含: 规则 id 列表, 读取的 Cassandra 数据表类型, 测点 id 列表等信息.

        :param rule_path:
        """
        self._rule_path = rule_path

    def load(self) -> list:
        with open(self._rule_path, 'r', encoding='utf-8') as r:
            config = r.read()
            if config is None:
                raise RuntimeError("config is None")
            return json.loads(config.strip('\t\r\n'))

    @staticmethod
    def point_ids(rule: dict) -> List[str]:
        """
        读取 rule 配置文件中的测点 id list

        :param rule: 规则配置
        :return: 测点 id list
        """
        points = rule['points']
        p_list = list()
        if points:
            for point in points:
                p_list.append(point.point_id)
        return p_list

    @staticmethod
    def datetime_format():
        return datetime_format()


class GraphParser(object):

    PROCESS_DATA_CASSANDRA_SOURCE = 'processCassandraSource'
    VIB_DATA_CASSANDRA_SOURCE = 'vibCassandraSource'
    INDEX_DATA_CASSANDRA_SOURCE = 'indexCassandraSource'

    def __init__(self,
                 file_path=None
                 ):
        """
        phm 规则编辑器 Cassandra, Kafka 等数据源配置信息解析

        :param file_path: 配置文件地址
        """
        self._file_path = file_path
        self.__graph_dict = None

    def load(self) -> Dict:
        with open(self._file_path, 'r', encoding='utf-8') as r:
            config = r.read()
            if config is None:
                raise RuntimeError("config is None")
            return json.loads(config.strip('\t\r\n'))

    def get_graph(self) -> Dict:
        """
        lazy create

        :return: graph dict
        """
        if self.__graph_dict is None:
            self.__graph_dict = self.load()
        return self.__graph_dict

    def _act_config(self, keys: Set) -> Dict:
        """
        actConfig 节点中读取 Cassandra, Kafka 配置信息

        :param keys: 需要读取的 keys
        :return:  配置信息 dict
        """
        graph = self.get_graph()
        res_dict = dict()
        if 'acts' not in graph:
            return res_dict
        acts = graph.get('acts')
        assert isinstance(acts, list)
        for act in acts:
            assert isinstance(act, dict)
            if 'actConfig' not in act:
                continue
            act_config = act.get('actConfig')
            assert isinstance(act_config, dict)
            for k, v in act_config.items():
                if k in keys:
                    res_dict[k] = v
        return res_dict

    def kafka_source_topics(self) -> Dict:
        """
        Kafka 相关的配置信息;

        包括 告警, indices指标, graph json 等 topic信息.

        :return:
        """
        # noinspection SpellCheckingInspection
        return self._act_config({'eventKafkaSource',
                                 'indiceKafkaSource',
                                 'graphKafkaSource',
                                 'exceptionKafkaSource',
                                 })

    def kafka_config(self) -> Dict:
        """
        kafka 配置信息, 默认多个 topic 的 kafka 集群的配置信息相同

        :return:
        """
        kafka_dict = self.kafka_source_topics()
        for source_name, kafka_config in kafka_dict.items():
            assert isinstance(kafka_config, dict)
            if kafka_config.__contains__('bootstraps') \
                    and kafka_config.__contains__('port'):
                return kafka_config

    def kafka_bootstraps(self) -> str:
        kafka_config = self.kafka_config()
        return '%s:%s' % (kafka_config['bootstraps'], kafka_config['port'])

    def cassandra_sources(self) -> Dict:
        """
        Cassandra 数据源及表配置信息;

        包括 振动表, 工艺表数据 .

        :return: Cassandra 表及数据源配置信息
        """
        return self._act_config({GraphParser.PROCESS_DATA_CASSANDRA_SOURCE,
                                 GraphParser.VIB_DATA_CASSANDRA_SOURCE,
                                 GraphParser.INDEX_DATA_CASSANDRA_SOURCE,
                                 })

    def process_window_duration(self) -> int:
        """
        返回 Cassandra 定期扫描的窗口长度

        :return: 数据扫描的窗口长度, seconds
        """
        return self._window_duration(GraphParser.PROCESS_DATA_CASSANDRA_SOURCE,
                                     'window_duration')

    def index_window_duration(self) -> int:
        return self._window_duration(GraphParser.INDEX_DATA_CASSANDRA_SOURCE,
                                     'window_duration')

    def index_slide_duration(self) -> int:
        return self._window_duration(GraphParser.INDEX_DATA_CASSANDRA_SOURCE,
                                     'slide_duration')

    def _window_duration(self, source_name, key):
        source_dict = self.cassandra_sources()
        if source_name in source_dict:
            source = source_dict.get(source_name)
            assert isinstance(source, dict)
            return source.get(key)

    def cassandra_process_table(self) -> str:
        return self._cassandra_table_name(GraphParser.PROCESS_DATA_CASSANDRA_SOURCE)

    def cassandra_index_table(self) -> str:
        return self._cassandra_table_name(GraphParser.INDEX_DATA_CASSANDRA_SOURCE)

    # noinspection SpellCheckingInspection
    def _cassandra_table_name(self, source_name):
        source_dict = self.cassandra_sources()
        if source_name in source_dict:
            process_dict = source_dict.get(source_name)
            assert isinstance(process_dict, dict)
            dt_names = process_dict.get('dtnames')
            assert isinstance(dt_names, list)
            return dt_names[0]

    def cassandra_config(self) -> Dict:
        """
        Cassandra 数据源配置信息, 默认振动表, 工艺表等共用一个 Cassandra 集群;

        :return: Cassandra 配置信息
        """
        source_dict = self.cassandra_sources()
        for source_name, source_config in source_dict.items():
            assert isinstance(source_config, dict)
            if source_config.__contains__('address') \
                    and source_config.__contains__('keyspace'):
                return source_config

    def cassandra_host(self) -> List:
        config = self.cassandra_config()
        if config.__contains__('address'):
            address = config['address']  # type: str
            return address.split(",")

    def cassandra_keyspace(self) -> str:
        config = self.cassandra_config()
        if config.__contains__('keyspace'):
            return config['keyspace']

    def start_time(self) -> str:
        c_sources = self.cassandra_sources()
        for _, c_sources in c_sources.items():
            if 'collect_to_current' in c_sources and int(c_sources['collect_to_current']) > 0:
                offset = int(c_sources['collect_to_current'])
                logger.info('collect_to_current: %s', offset)
                now_date = datetime.datetime.now()
                delta = datetime.timedelta(minutes=offset)
                start_date = now_date - delta
                return start_date.strftime(RuleParser.datetime_format())


def to_bool(v):
    # type: (Union[str, bool, None]) -> bool
    if v is None:
        return False
    if type(v) == bool:
        return v
    if type(v) == str:
        return v.lower() == 'true'
    return False


def datetime_format():
    return '%Y-%m-%d %H:%M:%S'


def date_format_str(date):
    # type: (datetime.datetime) -> str
    """
    格式化日期为字符串: %Y-%m-%d %H:%M:%S

    :param date: 日期
    :return: 格式化的日期字符串
    """
    if isinstance(date, datetime.datetime):
        return date.strftime(datetime_format())
    if isinstance(date, str):
        return date
    else:
        raise TypeError('expected datetime, but found %s' % type(date))


def parse_date(date_s: str) -> Optional[datetime.datetime]:
    """
    解析 %Y-%m-%d %H:%M:%S 为 datetime.datetime
    :param date_s: 日期字符串 %Y-%m-%d %H:%M:%S
    :return: 日期
    """
    if date_s:
        return datetime.datetime.strptime(date_s, datetime_format())
    return None


def to_dict(value):
    if isinstance(value, datetime.datetime):
        return datetime.datetime.strftime(value, '%Y-%m-%d %H:%M:%S.%f')[0:-3]
    else:
        return {k: v for k, v in value.__dict__.items() if not str(k).startswith('_')}


def json_contain(json_obj, keys: Sequence[str]):
    if json_obj is None or not keys:
        return False
    ele = json_obj
    for key in keys:
        if key not in ele:
            return False
        ele = ele[key]
    return True


def break_point(enable=True):
    if enable:
        import pydevd_pycharm
        pydevd_pycharm.settrace('localhost', port=12345, stdoutToServer=True, stderrToServer=True)

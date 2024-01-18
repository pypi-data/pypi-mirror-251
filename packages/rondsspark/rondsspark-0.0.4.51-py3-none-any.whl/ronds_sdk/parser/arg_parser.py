import datetime

import ujson

from ronds_sdk import error, logger_config
from ronds_sdk.parser import ArgParser
from ronds_sdk.tools import utils
from ronds_sdk.tools.constants import JsonKey

logger = logger_config.config()


class EditorArgParser(ArgParser):

    def __init__(self, file_path=None):
        super().__init__(file_path)
        self.activity = JsonKey.RULE_EDITOR_ACTIVITY.v

    @property
    def _act_config(self):
        # type: ('EditorArgParser') -> dict | str
        return self._act_configs[self.activity]

    def save_kafka_topics(self):
        # type: ('EditorArgParser') -> dict
        """
        Kafka 相关的配置信息 for rule editor;

        包括 告警, indices指标, graph json 等 topic信息.

        :return:
        """
        # noinspection SpellCheckingInspection
        keys = {'eventKafkaSource',
                'exceptionKafkaSource',
                'graphKafkaSource',
                'indiceKafkaSource',
                }
        acts_config = self._act_config
        res_dict = dict()
        for key in keys:
            if key in acts_config:
                res_dict[key] = acts_config.get(key)
        return res_dict

    def kafka_reader_topic(self):
        # type: () -> dict
        reader_kafka_key = JsonKey.KAFKA_READER_TOPIC.value
        act_config = self._act_config
        if reader_kafka_key not in act_config:
            raise error.KafkaError('missed kafka topic [readerKafkaSource] config: %s'
                                   % ujson.dumps(self.get_graph))
        return act_config.get(reader_kafka_key)

    def kafka_group_id(self):
        config = self.kafka_reader_topic()
        if JsonKey.KAFKA_GROUP_ID.value in config:
            return config.get(JsonKey.KAFKA_GROUP_ID.value)
        else:
            return self.get_worker_flow_id

    def kafka_bootstraps(self):
        # type: () -> str
        kafka_config = self.kafka_reader_topic()
        return '%s:%s' % (kafka_config['bootstraps'], kafka_config['port'])

    def cassandra_sources(self):
        # type: () -> dict
        """
        Cassandra 数据源及表配置信息;

        包括 振动表, 工艺表数据 .

        :return: Cassandra 表及数据源配置信息
        """
        names = {
            JsonKey.PROCESS_CASSANDRA_SOURCE.value,
            JsonKey.VIB_CASSANDRA_SOURCE.value
        }
        res_dict = dict()
        for n in names:
            if n in self._act_config:
                res_dict[n] = self._act_config[n]
        return res_dict

    # noinspection SpellCheckingInspection
    def cassandra_process_table(self):
        # type: () -> str
        process_dict = self._act_config[JsonKey.PROCESS_CASSANDRA_SOURCE.value]
        if process_dict is not None:
            assert isinstance(process_dict, dict)
            dt_names = process_dict.get('dtnames')
            assert isinstance(dt_names, list)
            return dt_names[0]

    def cassandra_config(self):
        # type: () -> dict
        """
        Cassandra 数据源配置信息, 默认振动表, 工艺表等共用一个 Cassandra 集群;

        :return: Cassandra 配置信息
        """
        source_dict = self.cassandra_sources()
        for source_name, source_config in source_dict.items():
            assert isinstance(source_config, dict)
            if 'address' in source_config \
                    and 'keyspace' in source_config:
                return source_config

    def cassandra_host(self):
        # type: () -> list
        config = self.cassandra_config()
        if 'address' in config:
            address = config['address']  # type: str
            return address.split(",")

    def cassandra_keyspace(self):
        # type: () -> str
        config = self.cassandra_config()
        if 'keyspace' in config:
            return config['keyspace']

    def window_duration(self):
        # type: () -> int
        """
        返回 Cassandra 定期扫描的窗口长度

        :return: 数据扫描的窗口长度, seconds
        """
        duration = self._act_config['window_duration']
        if duration is not None:
            return int(duration)
        return 300

    def window_slide_window(self):
        duration = self._act_config['window_slide_duration']
        if duration is not None:
            return int(duration)
        return 10

    def start_time(self):
        # type: () -> str
        collect_to_current = self._act_config['collect_to_current']
        if collect_to_current is not None:
            offset = int(collect_to_current)
            now_date = datetime.datetime.now()
            delta = datetime.timedelta(minutes=offset)
            start_date = now_date - delta
            return start_date.strftime(utils.datetime_format())


class RuleBaseArgParser(ArgParser):

    def __init__(self, file_path=None):
        super().__init__(file_path)

    def save_kafka_topics(self):
        # type: () -> dict
        """
        Kafka 相关的配置信息 for rule editor;

        包括 告警, indices指标, graph json 等 topic信息.

        :return:
        """
        # noinspection SpellCheckingInspection
        keys = {'eventKafkaSource': 'OnlineEventIssueActivity',
                'exceptionKafkaSource': 'OnlineExceptionToKafkaActivity',
                'indiceKafkaSource': 'OnlineIndicesToKafkaActivity',
                }
        res_dict = dict()
        for k, act in keys.items():
            if self._act_configs.get(act) is not None:
                res_dict[k] = self._act_configs[act]['kafkaSource']
        return res_dict

    def kafka_reader_topic(self):
        act_config = self._act_configs[JsonKey.KAFKA_SUBSRIBE_ACTIVITY.value]
        return act_config['kafkaSource']

    def kafka_group_id(self):
        config = self.kafka_reader_topic()
        if JsonKey.KAFKA_GROUP_ID.value in config:
            return config.get(JsonKey.KAFKA_GROUP_ID.value)
        else:
            return self.get_worker_flow_id

    def kafka_bootstraps(self):
        kafka_config = self.kafka_reader_topic()
        return '%s:%s' % (kafka_config['bootstraps'], kafka_config['port'])

    def redis_expire(self):
        config = self._act_configs[JsonKey.SAVE_REDIS_ACTIVITY.value]
        if 'saveTime' in config:
            return int(config['saveTime']) * 24 * 60 * 60

    def redis_source(self):
        config = self._act_configs[JsonKey.SAVE_REDIS_ACTIVITY.value]
        return config['redisSource']

    def redis_host(self):
        return self.redis_source()['address']

    def redis_dbname(self):
        return self.redis_source()['dbname']

    def redis_username(self):
        return self.redis_source()['username']

    def redis_password(self):
        return self.redis_source()['password']

    # noinspection PyBroadException
    def algorithm_config(self):
        # type: ('RuleBaseArgParser') -> str
        if JsonKey.ANALYTIC_ACTIVITY.v in self._act_configs:
            act = self._act_configs[JsonKey.ANALYTIC_ACTIVITY.v]
            if JsonKey.RONDS_API.v in act:
                ronds_api = act[JsonKey.RONDS_API.v]  # type: dict
                return ronds_api.get(JsonKey.GRAPH_CONFIG.v)

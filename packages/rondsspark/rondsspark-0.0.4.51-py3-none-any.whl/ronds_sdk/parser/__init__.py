from typing import Optional, Dict, Union

import ujson

from ronds_sdk import logger_config
from ronds_sdk.tools import utils
from ronds_sdk.tools.constants import JsonKey

logger = logger_config.config()


class Activity(object):

    def __init__(self, aid: str, act_name: str, act_config: str):
        self.aid = aid
        self.actName = act_name
        self._actConfig_str = act_config
        self._actConfig: Optional[Dict] = None

    def __repr__(self):
        return f'Activity(actName={self.actName}, aid={self.aid})'

    @property
    def act_config(self) -> Dict:
        if self._actConfig is None:
            self._actConfig = ujson.loads(self._actConfig_str)
        return self._actConfig

    def num_cpus(self):
        if 'calcConfig' in self.act_config:
            return self.act_config.get('calcConfig').get('num_cpus')

    def num_gpus(self):
        if 'calcConfig' in self.act_config:
            return self.act_config.get('calcConfig').get('num_gpus')

    def parallel(self):
        if 'calcConfig' in self.act_config:
            return self.act_config.get('calcConfig').get('parallel')

    def is_merge(self):
        if 'calcConfig' in self.act_config:
            return utils.to_bool(self.act_config.get('calcConfig').get('merge'))


class ArgParser(object):
    def __init__(self,  # type: ArgParser
                 file_path  # type: str
                 ):
        """
        phm 规则编辑器 Cassandra, Kafka 等数据源配置信息解析

        :param file_path: 配置文件地址
        """
        self._file_path = file_path
        self.__graph_dict = None
        self.__acts = None  # type: Optional[dict]

    def load(self):
        # type: ('ArgParser') -> dict
        with open(self._file_path, 'r', encoding='utf-8') as r:
            config = r.read()
            if config is None:
                raise RuntimeError("config is None")
            print("run arg: %s" % config.strip('\t\r\n'))
            return ujson.loads(config.strip('\t\r\n'))

    @property
    def get_graph(self):
        # type: ('ArgParser') -> dict
        """
        lazy create

        :return: graph dict
        """
        if self.__graph_dict is None:
            self.__graph_dict = self.load()
        return self.__graph_dict

    @property
    def get_worker_flow_id(self):
        # type: ('ArgParser') -> str
        return self.get_graph.get(JsonKey.WORKERFLOW_ID.value)

    @property
    def _act_configs(self):
        # type: ('ArgParser') -> dict[str, dict|None]
        """
        actConfig 节点中读取 Cassandra, Kafka 配置信息

        :return:  配置信息 dict
        """
        if self.__acts is None:
            self.__acts = dict()
            graph = self.get_graph
            res_dict = dict()
            if 'acts' not in graph:
                return res_dict
            acts = graph.get('acts')
            assert isinstance(acts, list)
            for act in acts:
                assert isinstance(act, dict)
                if 'actConfig' not in act:
                    continue
                self.__acts[act.get('actName')] = act.get('actConfig')
        return self.__acts

    def get_activities(self):
        activities = list()
        if 'acts' not in self.get_graph:
            return activities
        acts = self.get_graph.get('acts')
        for act in acts:
            activities.append(Activity(
                aid=act.get('id'),
                act_name=act.get('actName'),
                act_config=ujson.dumps(act.get('actConfig')) if act.get('actConfig') else None
            ))
        return activities

    def get_diagram(self) -> Dict:
        return self.get_graph.get('diagram')

    def _get_calc_config(self, key: str, default: Union[float, str]) -> Union[float, str]:
        try:
            return self.get_graph['calcConfig'][key]
        except KeyError:
            logger.warning("%s is None, return %f" % (key, default))
            return default

    def calc_config_is_merge(self):
        return utils.to_bool(self._get_calc_config('merge', True))

    def get_calc_config(self):
        return self._get_calc_config('num_cpus', 0.5), \
            self._get_calc_config('num_gpus', 0), \
            self._get_calc_config('parallel', 1), \
            self.calc_config_is_merge(),

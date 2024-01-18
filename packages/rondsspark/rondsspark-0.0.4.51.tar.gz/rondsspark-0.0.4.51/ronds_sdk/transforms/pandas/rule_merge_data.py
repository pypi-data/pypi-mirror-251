from collections import deque
from typing import Union, Dict, List, Optional, TYPE_CHECKING

from ronds_sdk.tools.constants import JsonKey, INDEX_DATA_TYPE
from ronds_sdk.tools.utils import json_contain

if TYPE_CHECKING:
    from ronds_sdk.models.data import IndexData, ProcessData


# noinspection SpellCheckingInspection
class RuleData(object):

    def __init__(self,
                 device_id,  # type: str
                 rule_ids,  # type: list[str]
                 nodes=None,  # type: list
                 edges=None,  # type: list
                 datasources=None,  # type: list
                 indices=None,  # type: list
                 events=None,  # type: list
                 running_time=None,  # type: float
                 datasource_times=None,  # type: str

                 ):
        """
        根据规则读取 Cassandra 数据, 组合成算法能够识别的 JSON 格式数据
        :param nodes: 设备 DAG nodes
        :param edges: 设备 DAG edges
        :param datasources: 数据源的具体数据
        :param indices: 需要存储到 Cassandra 的数据
        :param events: 需要发送到 Kafka 告警主题的数据
        :param running_time: 运行时间
        :param datasource_times: 数据源数据批次生成 时间
        """
        self._data_dict = {
            JsonKey.DEVICE_ID.value: device_id,
            'nodes': nodes if nodes else [
                {
                    'id': device_id,
                    'name': '',
                    'group': 2,
                    'code': 139555,
                    'attributes': {
                        'entcode': 'COM'
                    }
                }
            ],
            'edges': edges if edges else [],
            'datasource': [[]] if datasources is None else datasources,
            'version': '1.0.0',
            'indices': indices if indices else [],
            'events': events if events else [],
            'runningtime': running_time if running_time else [],
            'datasourcetimes': [datasource_times] if datasource_times else [],
            'rules': rule_ids,
            'cache': {
                JsonKey.DEVICE_ID.value: device_id,
                'metadata': [],
                'buffer': ''
            },
        }
        self._data_index = dict()
        self._empty = True

    def get_data(self) -> Optional[Dict]:
        if self._empty:
            return None
        datasources = self.get_datasource()
        for datasource in datasources:
            if json_contain(datasource, ('value', 'channeldata', 'data')):
                data = datasource['value']['channeldata']['data']
                for channel_data in data:
                    if isinstance(channel_data['times'], deque):
                        channel_data['times'] = list(channel_data['times'])
                    if isinstance(channel_data['values'], deque):
                        channel_data['values'] = list(channel_data['values'])
        return self._data_dict

    def get_datasource(self) -> List:
        datasources = self._data_dict['datasource']
        assert isinstance(datasources, list)
        return datasources[0]

    def set_nodes(self, nodes: List) -> None:
        if nodes:
            self._data_dict['nodes'] = nodes

    def set_edges(self, edges: List) -> None:
        if edges:
            self._data_dict['edges'] = edges

    def add_data(self, records: List, data_type: int):
        if INDEX_DATA_TYPE == data_type:
            for record in records:  # type: IndexData
                self._add_data(record.id,
                               record.time,
                               record.value,
                               data_type,
                               record.datatype)
        else:
            for record in records:  # type: ProcessData
                self._add_data(record.id,
                               record.time,
                               record.value,
                               data_type)

    def _add_data(self,
                  asset_id,  # type: str
                  c_time,  # type: str
                  value,  # type: Union[int, float]
                  data_type,  # type: int
                  index_code=-1,  # type: int
                  ):
        """
        添加工艺数据
        :param asset_id: 测点 id
        :param c_time: 数据产生时间
        :param value: 数据内容
        :param data_type: 数据类型, 默认工艺 data_type = 106, 特征值 data_type = 101
        :return: None
        """
        if asset_id is None or c_time is None or value is None:
            return
        if asset_id not in self._data_index:
            datasource = {
                'assetid': asset_id,
                'value': {
                    'channeldata': {
                        'code': '',
                        'nodetype': '',
                        'data': [],
                        'assetid': asset_id,
                        'caption': '',
                        'property': {
                            'sernortype': 0,
                            'direct': '',
                            'direction': 1
                        }
                    }
                }
            }
            self._data_index[asset_id] = datasource
            self.get_datasource().append(datasource)
            self._empty = False
        datasource = self._data_index[asset_id]
        self.fill_channel_data(data_type, asset_id, c_time,
                               value, index_code, datasource)

    @staticmethod
    def get_data_key(*args) -> str:
        return '_'.join([str(s) for s in args])

    def fill_channel_data(self,
                          data_type,  # type: int
                          asset_id,  # type: str
                          c_time,  # type: str
                          value,  # type: float
                          index_code,  # type: int
                          datasource,  # type: dict
                          ):
        """
        按照格式填充 datasource.value.chaneldata.data 的数据
        :param index_code 特征值编码
        :param value: 工艺数据值
        :param c_time: 数据产生时间
        :param asset_id: 测点 id
        :param data_type: 设备类型
        :param datasource: 需要填充的 datasource
        """
        channel_data_key = self.get_data_key(asset_id, data_type)
        if channel_data_key not in self._data_index:
            channel_data = {
                'times': deque(),
                'values': deque(),
                'datatype': data_type,
                'indexcode': index_code,
                'conditions': [],
                'properties': []
            }
            self._data_index[channel_data_key] = channel_data
            datasource['value']['channeldata']['data'].append(channel_data)
        channel_data = self._data_index[channel_data_key]
        channel_data['times'].appendleft(c_time)
        channel_data['values'].appendleft(value)

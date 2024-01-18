import uuid
from datetime import datetime
from typing import List

import ujson

from ronds_sdk.models.graph import Traceinfo, DatasourceValue, Datasource, Graph
from ronds_sdk.models.message import Message
from ronds_sdk.tools.data_utils import DataUtils


# noinspection SpellCheckingInspection
class GraphUtils(object):
    @staticmethod
    def get_graph(record: Message) -> Graph:
        # 一个切片一个设备
        record_message = record['_message']
        point_list = record_message['Childs']
        # 解析加入测量定义级数据
        point_parse_result = parse_point_data(point_list)
        datasource_list = point_parse_result["datasource_list"]
        wave_count = point_parse_result["wave_count"]

        # 解析加入设备级数据
        device_value = record_message['Value']
        datasource_list.append(parse_device_data(device_value))
        slicetime = parse_and_format_datetime(record_message['CreateTime'])
        datasource_times = [slicetime]
        datasource = [datasource_list]
        statistics = {'topicname': record['topic'], 'partition': record['partition'],
                      'offset': record['offset'], 'kafkatime': record['arrive_time'],
                      'deviceid': device_value['assetID'], 'wavecount': wave_count, 'datatime': slicetime}
        traceinfo: Traceinfo = {'site': record['topic'], 'arrivetimes': [record['arrive_time']]}
        graph: Graph = {
                'datasource': datasource,
                'datasourcetimes': datasource_times,
                'traceinfos': [traceinfo],
                'offset': record['offset'],
                'cache': {'buffer': "", 'metadata': [], 'deviceid': record['id']},
                'events': [[]],
                'indices': [[]],
                'statistics': statistics
            }
        if 'DataTag' in record_message:
            graph['graphid'] = record_message['DataTag']
        else:
            graph['graphid'] = str(uuid.uuid4())
        return graph


# noinspection SpellCheckingInspection
def parse_point_data(point_list):
    wave_count = 0
    data_source_list = []
    for point in point_list:
        point_value = point['Value']
        # 解析测点级数据
        point_property = DataUtils.convert_keys_to_lowercase(ujson.loads(point_value['Property']))
        point_data_list = point_value['Data']
        point_data_new_list = []
        for point_data in point_data_list:
            point_data_new_list.append(DataUtils.convert_keys_to_lowercase(ujson.loads(point_data)))
        point_channel_data: dict = {
            'assetid': point_value['assetID'],
            'caption': point_value['Caption'],
            'code': point_value['Code'],
            'nodetype': str(point_value['nodeType']),
            'property': point_property,
            'data': point_data_new_list
        }
        # 解析加入测量定义级数据
        vibdata = []
        pointid = point_value['assetID']
        measdef_list = point['Childs']
        for measdef in measdef_list:
            measdef_value = measdef['Value']
            measdef_property = DataUtils.convert_keys_to_lowercase(ujson.loads(measdef_value['Property']))
            measdef_data_list = measdef_value['Data']
            wave_data = get_data(measdef_data_list)
            measdef_new = {
                'assetid': measdef_value['assetID'],
                'caption': measdef_value['Caption'],
                'code': measdef_value['Code'],
                'nodetype': str(measdef_value['nodeType']),
                'property': measdef_property,
                'data': wave_data
            }
            vibdata.append(measdef_new)
            wave_count += len(wave_data)
        datasource_alue: DatasourceValue = {'measdefs': vibdata, 'channeldata': point_channel_data}
        data_source: Datasource = {'assetid': pointid, 'value': datasource_alue}
        data_source_list.append(data_source)
    parse_result = {'datasource_list': data_source_list, 'wave_count': wave_count}
    return parse_result


# noinspection SpellCheckingInspection
def parse_device_data(device_value):
    """
    解析设备级数据
    """
    device_data_list = device_value['Data']
    device_property = DataUtils.convert_keys_to_lowercase(ujson.loads(device_value['Property']))
    device_data_new_list = get_data(device_data_list)
    device_channel_data: dict = {
        'assetid': device_value['assetID'],
        'caption': device_value['Caption'],
        'code': device_value['Code'],
        'nodetype': str(device_value['nodeType']),
        'property': device_property,
        'data': device_data_new_list
    }
    data_source_value: DatasourceValue = {'measdefs': [], 'channeldata': device_channel_data}
    data_source: Datasource = {'assetid': device_value['assetID'], 'value': data_source_value}
    return data_source


# noinspection SpellCheckingInspection
def parse_and_format_datetime(time_str):
    formats = ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M%z"]
    for fmt in formats:
        try:
            dt = datetime.strptime(time_str, fmt)
            formatted_dt = dt.strftime("%Y-%m-%dT%H:%M:%S")
            return formatted_dt
        except ValueError:
            pass
    return None


def get_data(device_data_list) -> List[dict]:
    device_data_new_list = []
    for device_data in device_data_list:
        device_data_new_list.append(DataUtils.convert_keys_to_lowercase(ujson.loads(device_data)))
    return device_data_new_list

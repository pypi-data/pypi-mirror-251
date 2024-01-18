import datetime
from typing import List, Optional

import ujson

from ronds_sdk import logger_config
from ronds_sdk.datasources.minio_manager import MinioManager
from ronds_sdk.options.pipeline_options import MinioOptions
from ronds_sdk.tools.constants import JsonKey
from ronds_sdk.transforms.ray.base import RayTransform

logger = logger_config.config()


class TrendProcessIndexHandle(RayTransform):
    def __init__(self,  # type: TrendProcessIndexHandle
                 options=None,  # type: Optional[MinioOptions]
                 parallel=None,  # type: Optional[int]
                 num_cpus=0.5,  # type: float
                 num_gpus=0,  # type: float
                 worker_index=-1,  # type: int
                 ):
        # type: (...) -> None
        super().__init__(worker_index,
                         parallel=parallel,
                         num_cpus=num_cpus,
                         num_gpus=num_gpus,
                         options=options)
        self._statistics_dict = None  # type: Optional[dict]
        self.minio_sources = None  # type: Optional[MinioManager]
        self.options = options

    def pre_startup(self):
        super().pre_startup()
        self._statistics_dict = dict()
        if not self.minio_sources:
            self.minio_sources = MinioManager(self.options)

    # noinspection SpellCheckingInspection
    async def process(self, inputs):
        # type: ('TrendProcessIndexHandle', dict[str, str|List[str]]) -> str|List[str]|None
        for p_name, records_str in inputs.items():
            kafka_msg = ujson.loads(records_str)
            records = kafka_msg[JsonKey.MESSAGE.value]
            # records = [record for record in records if not math.isnan(record['Value'])]
            aggregated_data = {}
            for record in records:
                assetid = record["Id"]
                measdate = record["Time"]
                measvalue = record["Value"]
                # 取前13个字符，即年月日时部分
                hour = measdate[:13]
                # 判断是否是过期数据，过期数据直接丢弃
                if not self._judge_effective(hour, assetid):
                    continue
                # 检查是否已存在该小时的聚合数据，如果不存在则创建并初始化
                self._get_current_data(aggregated_data, assetid, hour, measvalue)
            for (id_value, time_value), new_cache_data in aggregated_data.items():
                new_cache_data["avg"] = new_cache_data["sum"] / new_cache_data["count"]
                new_kafka_msg = self._set_cache(id_value, kafka_msg, new_cache_data, time_value)
                if new_kafka_msg:
                    yield ujson.dumps(new_kafka_msg)

    # noinspection SpellCheckingInspection
    @staticmethod
    def _get_current_data(aggregated_data, assetid, hour, measvalue):
        if (assetid, hour) not in aggregated_data:
            aggregated_data[(assetid, hour)] = {
                "assetid": assetid,
                "hour": hour,
                "sum": 0.0,
                "count": 0,
                "avg": 0.0,
            }
        aggregated_data[(assetid, hour)]["sum"] += measvalue
        aggregated_data[(assetid, hour)]["count"] += 1
        if 'max' not in aggregated_data[(assetid, hour)] or aggregated_data[(assetid, hour)]['max'] < measvalue:
            aggregated_data[(assetid, hour)]['max'] = measvalue
        if 'min' not in aggregated_data[(assetid, hour)] or aggregated_data[(assetid, hour)]['min'] > measvalue:
            aggregated_data[(assetid, hour)]['min'] = measvalue

    def _set_cache(self, id_value, kafka_msg, new_cache_data, time_h):
        new_kafka_msg = None
        if id_value in self._statistics_dict:
            if time_h in self._statistics_dict[id_value]:
                cache_data = self._statistics_dict[id_value][time_h]
                new_cache_data = self.init_cache_data(cache_data=cache_data, new_cache_data=new_cache_data)
                new_cache_data['partitionId'] = kafka_msg[JsonKey.PARTITION.value]
                new_cache_data['offset'] = kafka_msg[JsonKey.OFFSET.value]
                self._statistics_dict[id_value][time_h] = new_cache_data

            else:
                self._statistics_dict[id_value][time_h] = \
                    self.init_cache_data(cache_data=new_cache_data, kafka_msg=kafka_msg)
                prev_time, prev_time_h = self._get_prev_time(time_h)
                if prev_time_h in self._statistics_dict[id_value]:
                    prev_cache_data = self._statistics_dict[id_value][prev_time_h]
                    self._get_send_msg(id_value, kafka_msg, prev_cache_data, prev_time)
                    del self._statistics_dict[id_value][prev_time_h]
                    new_kafka_msg = kafka_msg
        else:
            self._statistics_dict[id_value] = dict()
            self._statistics_dict[id_value][time_h] = \
                self.init_cache_data(cache_data=new_cache_data, kafka_msg=kafka_msg)
        return new_kafka_msg

    @staticmethod
    def _get_time(time_h):
        if 'T' in time_h:
            time = datetime.datetime.strptime(time_h, '%Y-%m-%dT%H')
        else:
            time = datetime.datetime.strptime(time_h, '%Y-%m-%d %H')
        return time

    @staticmethod
    def _get_prev_time(time_h):
        if 'T' in time_h:
            prev_time = datetime.datetime.strptime(time_h, '%Y-%m-%dT%H') - datetime.timedelta(hours=2)
            prev_time_h = prev_time.strftime('%Y-%m-%dT%H')
        else:
            prev_time = datetime.datetime.strptime(time_h, '%Y-%m-%d %H') - datetime.timedelta(hours=2)
            prev_time_h = prev_time.strftime('%Y-%m-%d %H')
        return prev_time, prev_time_h

    @staticmethod
    def init_cache_data(cache_data, new_cache_data=None, kafka_msg=None):
        init_cache_data = dict()
        if new_cache_data:
            init_cache_data['min'] = new_cache_data['min'] if new_cache_data['min'] < cache_data['min'] \
                else cache_data['min']
            init_cache_data['max'] = new_cache_data['max'] if new_cache_data['max'] > cache_data['max'] \
                else cache_data['max']
            init_cache_data['count'] = new_cache_data['count'] + cache_data['count']
            init_cache_data['avg'] = ((new_cache_data['avg'] * new_cache_data['count']
                                       + cache_data['avg'] * cache_data['count']) / init_cache_data['count'])
        else:
            init_cache_data['min'] = cache_data['min']
            init_cache_data['max'] = cache_data['max']
            init_cache_data['count'] = cache_data['count']
            init_cache_data['avg'] = cache_data['avg']
        if kafka_msg:
            init_cache_data['partitionId'] = kafka_msg[JsonKey.PARTITION.value]
            init_cache_data['offset'] = kafka_msg[JsonKey.OFFSET.value]
        return init_cache_data

    @staticmethod
    def _get_send_msg(id_value, kafka_msg, prev_cache_data, prev_time):
        send_msg = dict()
        send_msg['id'] = id_value
        # 将时间转换为带时区的字符串格式，设置时区为 UTC+8
        timezone = datetime.timezone(datetime.timedelta(hours=0))
        time_with_timezone = prev_time.replace(tzinfo=timezone).strftime('%Y-%m-%dT%H:00:00%z')
        send_msg['time'] = time_with_timezone
        send_msg['partitionId'] = prev_cache_data['partitionId']
        send_msg['offset'] = prev_cache_data['offset']
        del prev_cache_data['partitionId'], prev_cache_data['offset']
        send_msg['value'] = prev_cache_data
        kafka_msg[JsonKey.MESSAGE.value] = send_msg
        kafka_msg[JsonKey.ID.value] = id_value

    def _judge_effective(self, hour, id_value):
        time = self._get_time(hour)
        if id_value in self._statistics_dict and hour not in self._statistics_dict[id_value]:
            effect_flags = [time < self._get_time(cache_time_h)
                            for cache_time_h in self._statistics_dict[id_value].keys()]
            if len(effect_flags) > 0 and False not in effect_flags:
                return False
        return True


class TrendTsDatasIndexHandle(TrendProcessIndexHandle):
    def __init__(self,  # type: TrendTsDatasIndexHandle
                 options=None,  # type: Optional[MinioOptions]
                 parallel=None,  # type: Optional[int]
                 num_cpus=0.5,  # type: float
                 num_gpus=0,  # type: float
                 worker_index=-1,  # type: int
                 ):
        # type: (...) -> None
        super().__init__(parallel=parallel,
                         num_cpus=num_cpus,
                         num_gpus=num_gpus,
                         options=options,
                         worker_index=worker_index)

    # noinspection SpellCheckingInspection
    async def process(self, inputs):
        # type: ('TrendTsDatasIndexHandle', dict[str, str|List[str]]) -> str|List[str]|None
        for p_name, records_str in inputs.items():
            kafka_msg = ujson.loads(records_str)
            records = kafka_msg[JsonKey.MESSAGE.value]
            # records = [record for record in records if not math.isnan(record['Value'])]
            aggregated_data = {}
            for record in records:
                assetid = record["assetid"]
                measdate = record["measdate"]
                measvalue = record["measvalue"]
                hour = measdate[:13]  # 取前13个字符，即年月日时部分
                # 判断是否是过期数据，过期数据直接丢弃
                if not self._judge_effective(hour, assetid):
                    continue
                self._get_current_data(aggregated_data, assetid, hour, measvalue)  # 检查是否已存在该小时的聚合数据，如果不存在则创建并初始化
            for (id_value, time_value), new_cache_data in aggregated_data.items():
                new_cache_data["avg"] = new_cache_data["sum"] / new_cache_data["count"]
                new_kafka_msg = self._set_cache(id_value, kafka_msg, new_cache_data, time_value)
                if new_kafka_msg:
                    yield ujson.dumps(new_kafka_msg)


class TrendFeatureDatasIndexHandle(TrendProcessIndexHandle):
    def __init__(self,  # type: TrendFeatureDatasIndexHandle
                 options=None,  # type: Optional[MinioOptions]
                 parallel=None,  # type: Optional[int]
                 num_cpus=0.5,  # type: float
                 num_gpus=0,  # type: float
                 worker_index=-1,  # type: int
                 ):
        # type: (...) -> None
        super().__init__(parallel=parallel,
                         num_cpus=num_cpus,
                         num_gpus=num_gpus,
                         options=options,
                         worker_index=worker_index)

    # noinspection SpellCheckingInspection
    async def process(self, inputs):
        # type: ('TrendFeatureDatasIndexHandle', dict[str, str|List[str]]) -> str|List[str]|None
        for p_name, records_str in inputs.items():
            kafka_msg = ujson.loads(records_str)
            records = kafka_msg[JsonKey.MESSAGE.value]
            # records = [record for record in records if not math.isnan(record['Value'])]
            aggregated_data = {}
            for record in records:
                assetid = record["assetid"]
                measdate = record["measdate"]
                measvalue = record["measvalue"]
                datatype = record['datatype']
                hour = measdate[:13]  # 取前13个字符，即年月日时部分
                # 判断是否是过期数据，过期数据直接丢弃
                if not self._judge_effective_datatype(datatype, hour, assetid):
                    continue
                # 检查是否已存在该小时的聚合数据，如果不存在则创建并初始化
                self._get_current_data_with_datatype(aggregated_data, assetid, datatype, hour, measvalue)
            for (id_value, data_type, time_value), new_cache_data in aggregated_data.items():
                new_cache_data["avg"] = new_cache_data["sum"] / new_cache_data["count"]
                new_kafka_msg = \
                    self._set_datatype_cache(id_value, kafka_msg, new_cache_data, time_value, data_type)
                if new_kafka_msg:
                    yield ujson.dumps(new_kafka_msg)

    # noinspection SpellCheckingInspection
    @staticmethod
    def _get_current_data_with_datatype(aggregated_data, assetid, datatype, hour, measvalue):
        if (assetid, datatype, hour) not in aggregated_data:
            aggregated_data[(assetid, datatype, hour)] = {
                "assetid": assetid,
                "datatype": datatype,
                "hour": hour,
                "sum": 0.0,
                "count": 0,
                "avg": 0.0,
            }
        aggregated_data[(assetid, datatype, hour)]["sum"] += measvalue
        aggregated_data[(assetid, datatype, hour)]["count"] += 1
        if ('max' not in aggregated_data[(assetid, datatype, hour)]
                or aggregated_data[(assetid, datatype, hour)]['max'] < measvalue):
            aggregated_data[(assetid, datatype, hour)]['max'] = measvalue
        if ('min' not in aggregated_data[(assetid, datatype, hour)]
                or aggregated_data[(assetid, datatype, hour)]['min'] > measvalue):
            aggregated_data[(assetid, datatype, hour)]['min'] = measvalue

    def _set_datatype_cache(self, id_value, kafka_msg, new_cache_data, time_h, data_type):
        new_kafka_msg = None
        if id_value in self._statistics_dict:
            if data_type in self._statistics_dict[id_value]:
                if time_h in self._statistics_dict[id_value][data_type]:
                    cache_data = self._statistics_dict[id_value][data_type][time_h]
                    new_cache_data = self.init_cache_data(cache_data=cache_data, new_cache_data=new_cache_data)
                    self._statistics_dict[id_value][data_type][time_h] = new_cache_data
                else:
                    self._statistics_dict[id_value][data_type][time_h] = \
                        self.init_cache_data(cache_data=new_cache_data, kafka_msg=kafka_msg)
                    prev_time, prev_time_h = self._get_prev_time(time_h)
                    if prev_time_h in self._statistics_dict[id_value][data_type]:
                        prev_cache_data = self._statistics_dict[id_value][data_type][prev_time_h]
                        self._get_send_msg(id_value, kafka_msg, prev_cache_data, prev_time)
                        del self._statistics_dict[id_value][data_type][prev_time_h]
                        new_kafka_msg = kafka_msg
            else:
                self._statistics_dict[id_value][data_type] = dict()
                self._statistics_dict[id_value][data_type][time_h] = \
                    self.init_cache_data(cache_data=new_cache_data, kafka_msg=kafka_msg)
        else:
            self._statistics_dict[id_value] = dict()
            self._statistics_dict[id_value][data_type] = dict()
            self._statistics_dict[id_value][data_type][time_h] = \
                self.init_cache_data(cache_data=new_cache_data, kafka_msg=kafka_msg)
        return new_kafka_msg

    def _judge_effective_datatype(self, datatype, hour, id_value):
        time = self._get_time(hour)
        if (id_value in self._statistics_dict and datatype in self._statistics_dict[id_value]
                and hour not in self._statistics_dict[id_value][datatype]):
            effect_flags = [time < self._get_time(cache_time_h)
                            for cache_time_h in self._statistics_dict[id_value][datatype].keys()]
            if len(effect_flags) > 0 and False not in effect_flags:
                return False
        return True


class TrendTraitDatasIndexHandle(TrendFeatureDatasIndexHandle):
    def __init__(self,  # type: TrendTraitDatasIndexHandle
                 options=None,  # type: Optional[MinioOptions]
                 parallel=None,  # type: Optional[int]
                 num_cpus=0.5,  # type: float
                 num_gpus=0,  # type: float
                 worker_index=-1,  # type: int
                 ):
        # type: (...) -> None
        super().__init__(parallel=parallel,
                         num_cpus=num_cpus,
                         num_gpus=num_gpus,
                         options=options,
                         worker_index=worker_index)

    # noinspection SpellCheckingInspection
    async def process(self, inputs):
        # type: ('TrendTraitDatasIndexHandle', dict[str, str|List[str]]) -> str|List[str]|None
        for p_name, records_str in inputs.items():
            kafka_msg = ujson.loads(records_str)
            records = kafka_msg[JsonKey.MESSAGE.value]
            # records = [record for record in records if not math.isnan(record['Value'])]
            aggregated_data = {}
            for record in records:
                assetid = record["Id"]
                measdate = record["Time"]
                measvalue = record["Value"]
                datatype = record['DataType']
                hour = measdate[:13]  # 取前13个字符，即年月日时部分
                # 判断是否是过期数据，过期数据直接丢弃
                if not self._judge_effective_datatype(datatype, hour, assetid):
                    continue
                # 检查是否已存在该小时的聚合数据，如果不存在则创建并初始化
                self._get_current_data_with_datatype(aggregated_data, assetid, datatype, hour, measvalue)
            for (id_value, data_type, time_value), new_cache_data in aggregated_data.items():
                new_cache_data["avg"] = new_cache_data["sum"] / new_cache_data["count"]
                new_kafka_msg = self._set_datatype_cache(id_value, kafka_msg, new_cache_data, time_value,
                                                         data_type)
                if new_kafka_msg:
                    yield ujson.dumps(new_kafka_msg)

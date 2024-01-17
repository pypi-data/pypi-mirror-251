import asyncio
import datetime
import json
from typing import List

import pandas as pd

from ronds_sdk import logger_config, PipelineOptions
from ronds_sdk.options.pipeline_options import AlgorithmOptions
from ronds_sdk.tools import utils
from ronds_sdk.tools.cache import ExpireCache
from ronds_sdk.tools.constants import JsonKey
from ronds_sdk.tools.utils import RuleParser
from ronds_sdk.tools.window import WindowDF
from ronds_sdk.transforms import ronds
from ronds_sdk.transforms.pandas.rule_merge_data import RuleData
from ronds_sdk.transforms.pandas.transforms import Algorithm
from ronds_sdk.transforms.ray.base import RayTransform

logger = logger_config.config()


class RuleAlgorithm(RayTransform):

    def __init__(self,  # type: RuleAlgorithm
                 rules,  # type: list[dict] # 规则集合
                 options,  # type: PipelineOptions
                 dt_column,  # type: str  # 时间字段
                 id_column="id",  # type: str
                 measure_column="Value",  # type: str
                 parallel=None,  # type: int
                 worker_index=-1,  # type: int
                 ):
        super().__init__(worker_index, parallel=parallel)
        self._options = options.view_as(AlgorithmOptions)
        self.rules = rules
        self.dt_column = dt_column
        self._id_column = id_column
        self._measure_column = measure_column
        self.rule_groups = set()
        self.algorithm = Algorithm(
            ronds.Algorithm(self._options.get_alg_path(), self._options.get_alg_func()),
            self._options)
        self.window_buffer = WindowDF(self._options.get_window_duration(),
                                      self._options.get_window_slide_duration())

    async def consume(self):
        """
        从上游消费最新数据, 缓存到本地 buffer
        :return: 常驻任务, 不结束, 无返回值
        """
        data_cache = dict()
        dt_cache = dict()
        while True:
            logger.debug("consume next start, current_refs if None: %s" % (self.current_refs is None))
            current_dict = await self.fetch_currents(no_wait=True)
            self._put_cache(current_dict, data_cache, dt_cache)
            if self.window_buffer.should_schedule():
                self._append_window_buffer(data_cache, dt_cache)
                df_res = self.window_buffer.query()
                await self.alg_process(df_res)
            if utils.collection_empty(current_dict):
                await asyncio.sleep(1)

    async def alg_process(self, df_dict):
        # type: (dict[str, pd.DataFrame]) -> None
        if utils.collection_empty(df_dict):
            return
        for rule_group in self.rule_groups:
            rule = self.rules[rule_group]
            device_id = rule.get(JsonKey.ASSET_ID.value)
            rule_id_list = RuleParser.rule_ids(rule)
            point_id_list = RuleParser.point_ids(rule)
            rule_data = RuleData(device_id, rule_id_list, desc=False)
            self._rule_data_process(rule_data, point_id_list, df_dict)
            alg_res = self._alg_call(rule_data)
            await self.buffer.put(alg_res)

    @staticmethod
    def _rule_data_process(rule_data, point_id_list, df_dict):
        # type: (RuleData, list, dict[str, pd.DataFrame]) -> None
        for point_id in point_id_list:
            if not df_dict.__contains__(point_id):
                continue
            df = df_dict[point_id]
            for dt, row in df.iterrows():
                rule_data.add_process_data(point_id, str(dt), row.get('v'))

    def _alg_call(self, rule_data):
        # type: (RuleData) -> str | None
        data_dict = rule_data.get_data()
        alg_dict = self.algorithm.algorithm_call(data_dict)
        return json.dumps(alg_dict)

    def _append_window_buffer(self, data_cache, dt_cache):
        # type: (dict, dict[str, List[str]]) -> None
        for asset_id, dt_list in dt_cache.items():
            if len(dt_list) == 0:
                continue
            data = data_cache[asset_id]
            self.window_buffer.append(data, dt_list, asset_id)
        # clear cache
        self._clean_cache(data_cache, dt_cache)

    def _put_cache(self, current_dict, data_cache, dt_cache):
        # type: (dict[str, str], dict, dict[str, List[str]]) -> None
        """
        定期缓存数据, 批次存储到 WindowDF 进行处理
        :param current_dict:
        :param data_cache: 数据格式如下:
                {
                  "$asset_id": {
                    "v": []
                  }
                }

        :param dt_cache: 数据格式如下:
                {
                    "$asset_id": []
                }

        :return:
        """
        if utils.collection_empty(current_dict):
            return
        for input_name, input_data_str in current_dict.items():
            input_dict = json.loads(input_data_str)
            assert isinstance(input_dict, dict)
            asset_id = input_dict[self._id_column]
            dt = input_dict[self.dt_column]
            rule_group = input_dict[JsonKey.RULE_GROUP.value]
            if rule_group is None:
                continue
            self.rule_groups.add(rule_group)
            if asset_id is None or dt is None:
                continue
            if not data_cache.__contains__(asset_id):
                data_cache[asset_id] = {
                    "v": []
                }
            if not dt_cache.__contains__(asset_id):
                dt_cache[asset_id] = []
            data_cache[asset_id]['v'].append(input_dict[self._measure_column])
            dt_cache[asset_id].append(dt)

    @staticmethod
    def _clean_cache(data_cache, dt_cache):
        # type: (dict[str, dict[str, list]], dict[str, list]) -> None
        for dt_list in dt_cache.values():
            dt_list.clear()
        for data_dict in data_cache.values():
            for d_list in data_dict.values():
                d_list.clear()

    def get_dt_or_now(self, json_dict):
        # type: (dict) -> str
        """
        获取数据的日期, 若不存在, 则取当前日期
        :param json_dict: 数据
        :return: 日期
        """
        if self.dt_column is None or not json_dict.__contains__(self.dt_column):
            return datetime.datetime.now().strftime(utils.datetime_format())
        return json_dict.get(self.dt_column)






import datetime
from typing import Dict, Optional, Callable

import pandas as pd
from sortedcontainers import SortedList

from ronds_sdk import logger_config
from ronds_sdk.tools import utils

__all__ = [
    'WindowDF',
    'WindowSortedList',
]


logger = logger_config.config()
default_partition = "_df"


class WindowDF(object):

    def __init__(self, window_duration, window_slide_duration):
        """
        使用时间序列作为索引, 创建包含时间区间的 DataFrame
        :param window_duration:  DataFrame 包含窗口时间的长度, seconds
        :param window_slide_duration: DataFrame 窗口的滑动时间, seconds
        """
        self._window_duration = window_duration
        self._window_slide_duration = window_slide_duration
        self._window_slide_duration_delta = datetime.timedelta(seconds=window_slide_duration)
        self.start_time = '2020-01-01 00:00:00'
        self._time_cursor = None  # type: Optional[datetime.datetime]
        # noinspection PyTypeChecker
        self.df = dict()  # type: dict[str, pd.DataFrame]

    def update_time_cursor(self):
        """
        更新当前日期游标, 位移步长: self._window_slide_duration
        :return: 更新后的游标日期
        """
        if self._time_cursor is None:
            self._time_cursor = datetime.datetime.now()
        else:
            self._time_cursor += datetime.timedelta(seconds=self._window_slide_duration)
        now_dt = datetime.datetime.now()
        if self._time_cursor > now_dt:
            logger.warn("_time_cursor [%s] is greater than now [%s]"
                        % (utils.date_str(self._time_cursor), utils.date_str(now_dt)))
            self._time_cursor = now_dt
        return self._time_cursor

    def append(self, data, dt_times, partition=default_partition):
        # type: (dict, list, str) -> None
        if utils.collection_empty(data) or utils.collection_empty(dt_times):
            return
        dt_series = pd.to_datetime(pd.Series(dt_times))
        incr_df = pd.DataFrame(data, index=dt_series)
        if partition not in self.df:
            self.df[partition] = incr_df
        else:
            self.df[partition] = self._merge(self.df[partition], incr_df)

    def query(self) -> Dict[str, 'pd.DataFrame']:
        """
        更新游标日期后, 查询 [游标日期 - 窗口间隔, 游标日期] 范围内的数据, 并淘汰过期数据
        :return:
        """
        time_cursor = self.update_time_cursor()
        expire_date = self._time_cursor - datetime.timedelta(seconds=self._window_duration)
        self._evict_expire(expire_date)
        res_dict = dict()
        for part, df in self.df.items():
            query_res = df[expire_date:time_cursor]  # type: pd.DataFrame
            if not query_res.empty:
                res_dict[part] = query_res
                logger.debug("[%s : %s] part: %s, size: %d"
                             % (utils.date_str(expire_date),
                                utils.date_str(time_cursor),
                                part, len(res_dict[part])))
        return res_dict

    def should_schedule(self, dt_cache=None):
        """
        当前日期 - 游标日期 > 滑动间隔, 返回 True
        :return:
        """
        if self._time_cursor is None:
            if utils.collection_empty(dt_cache):
                self._time_cursor = datetime.datetime.now()
            else:
                self._time_cursor = utils.str_date(dt_cache.values()[0])
        # todo 取 dt_cache 中最大时间代替 now
        interval = datetime.datetime.now() - self._time_cursor
        return interval > self._window_slide_duration_delta

    @staticmethod
    def _merge(df, inc_df):
        # type: (pd.DataFrame, str) -> None
        df = pd.concat([df, inc_df], copy=False)
        df.sort_index(inplace=True, kind="mergesort")
        return df

    def _evict_expire(self, expire_date):
        if self.df is None:
            return
        expire_date_str = expire_date.strftime(utils.datetime_format())
        for partition, df in self.df.items():
            df.drop([self.start_time, expire_date_str], inplace=True, errors='ignore')


class WindowSortedList(object):
    def __init__(self,
                 window_duration: int,
                 window_slide_duration: int,
                 sorted_key: Callable
                 ):
        """
        使用 SortedList 实现排序的时间窗口
        :param window_duration:  SortedList 包含窗口时间的长度, seconds
        :param window_slide_duration: SortedList 包含窗口的滑动时间, seconds
        :param sorted_key: 提取数据的排序 key 的函数
        """
        self._window_duration = window_duration
        self._window_slide_duration = window_slide_duration
        self._sorted_key = sorted_key
        self._window_slide_duration_delta = datetime.timedelta(seconds=window_slide_duration)
        self._window_duration_delta = datetime.timedelta(seconds=self._window_duration)
        self._time_cursor = None  # type: Optional[datetime.datetime]
        self.cache = dict()  # type: Dict[str, SortedList]

    def update_time_cursor(self):
        if self._time_cursor is None:
            self._time_cursor = datetime.datetime.now()
        else:
            self._time_cursor += self._window_slide_duration_delta
        now_dt = datetime.datetime.now()
        if self._time_cursor > now_dt:
            logger.warn("_time_cursor [%s] is greater than now [%s]"
                        % (utils.date_str(self._time_cursor), utils.date_str(now_dt)))
            self._time_cursor = now_dt
        return self._time_cursor

    def append(self, data: Dict, partition: str = default_partition):
        if utils.collection_empty(data):
            return
        self.cache.setdefault(partition, SortedList(key=self._sorted_key)).append(data)

    def query(self):
        expire_date = self._time_cursor - datetime.timedelta(seconds=self._window_duration)
        self._evict_expire(expire_date)
        res_dict = dict()
        for part, sorted_list in self.cache.items():
            index = sorted_list.bisect_right(self._time_cursor)
            if index <= 0:
                continue
            query_res = sorted_list[:index]
            if not utils.collection_empty(query_res):
                res_dict[part] = query_res
        return res_dict

    def should_schedule(self, record: Dict):
        if self._time_cursor is None:
            self._time_cursor = self._sorted_key(record)

        interval = self._sorted_key(record) - self._time_cursor
        is_schedule = interval > self._window_slide_duration_delta
        if is_schedule:
            self.update_time_cursor()
        return is_schedule

    def _evict_expire(self, expire_date):
        if self.cache is None:
            return
        for _, sorted_list in self.cache.items():
            index = sorted_list.bisect_right(expire_date)
            if index > 0:
                del sorted_list[:index]

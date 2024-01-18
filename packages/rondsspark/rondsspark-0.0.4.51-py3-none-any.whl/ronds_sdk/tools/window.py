import datetime
import pandas as pd

from ronds_sdk import logger_config
from ronds_sdk.tools import utils

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
        self.start_time = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")
        # noinspection PyTypeChecker
        self._time_cursor = None  # type: datetime.datetime
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
        if not self.df.__contains__(partition):
            self.df[partition] = incr_df
        else:
            self.df[partition] = self._merge(self.df[partition], incr_df)

    def query(self):
        # type: () -> dict[str, pd.DataFrame]
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

    def should_schedule(self):
        """
        当前日期 - 游标日期 > 滑动间隔, 返回 True
        :return:
        """
        if self._time_cursor is None:
            self._time_cursor = datetime.datetime.now()
        return datetime.datetime.now() - self._time_cursor > self._window_slide_duration_delta

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

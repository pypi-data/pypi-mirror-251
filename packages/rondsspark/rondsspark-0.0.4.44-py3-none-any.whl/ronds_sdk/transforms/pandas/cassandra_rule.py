import datetime
import json
import logging
import time
import traceback
from typing import List, Dict, Optional, Tuple

import pandas as pd

from ronds_sdk import error, logger_config, PipelineOptions
from ronds_sdk.datasources.cassandra_manager import ProcessDataManager, IndexDataManager, QueryManager
from ronds_sdk.options.pipeline_options import CassandraOptions, CassandraWindowOptions
from ronds_sdk.tools.constants import PROCESS_DATA_TYPE, INDEX_DATA_TYPE
from ronds_sdk.tools.utils import WrapperFunc, Singleton, parse_date, date_format_str
from ronds_sdk.transforms.pandas.rule_merge_data import RuleData

logger_config.config()
logger = logging.getLogger('executor')


class Scheduler:
    def __init__(self,
                 end_datetime: datetime.datetime,
                 window_duration: int,
                 slide_duration: int,
                 query_manager: QueryManager,
                 ):
        self.end_datetime = end_datetime
        self.window_delta = datetime.timedelta(seconds=window_duration)
        self.slide_delta = datetime.timedelta(seconds=slide_duration)
        self.query_manager = query_manager

    def update_next(self):
        # different from "lib: schedule"
        self.end_datetime = self.end_datetime + self.slide_delta

    def start_time(self):
        return self.end_datetime - self.window_delta

    def should_start(self):
        return datetime.datetime.now() > self.end_datetime


class ForeachRule(object, metaclass=Singleton):
    def __init__(self,
                 options,  # type: PipelineOptions
                 action_func,  # type: WrapperFunc
                 ):
        self.c_options = options.view_as(CassandraOptions)
        self.cw_options = options.view_as(CassandraWindowOptions)
        self.action_func = action_func

    def foreach_rules(self,
                      rules,
                      ):
        logger.info("foreach_rules started ~")
        current_timestamp = (datetime.datetime.now()
                             if self.c_options.cassandra_start_datetime is None
                             else parse_date(self.c_options.cassandra_start_datetime))
        process_window_duration = int(self.cw_options.process_data_window_duration)
        index_window_duration = int(self.cw_options.index_data_window_duration)
        index_slide_duration = int(self.cw_options.index_data_slide_duration)

        # iter to tuple
        rules = [r for r in rules]
        schedulers = {
            PROCESS_DATA_TYPE: Scheduler(current_timestamp,
                                         process_window_duration,
                                         process_window_duration,
                                         ProcessDataManager(self.c_options)),
            INDEX_DATA_TYPE: Scheduler(current_timestamp,
                                       index_window_duration,
                                       index_slide_duration,
                                       IndexDataManager(self.c_options)),
        }

        while True:
            # noinspection PyBroadException
            try:
                for data_type, scheduler in schedulers.items():
                    if not scheduler.should_start():
                        continue
                    logger.debug("running pending ~")
                    self.rule_task(rules=rules,
                                   scheduler=scheduler,
                                   data_type=data_type,
                                   action_func=self.action_func)
                    scheduler.update_next()
            except error.KafkaError:
                logging.error("rule_task kafka error: \n%s" % traceback.format_exc())
            except Exception:
                logging.error("rule_task error: \n%s" % traceback.format_exc())
            finally:
                time.sleep(2)

    def rule_task(self,
                  rules,
                  scheduler,  # type: Scheduler
                  data_type,  # type: int
                  action_func,  # type: WrapperFunc
                  ):
        start_datetime = scheduler.start_time()
        end_datetime = scheduler.end_datetime
        start_datetime_str = date_format_str(start_datetime)
        end_datetime_str = date_format_str(end_datetime)
        query_manager = scheduler.query_manager
        # process rules
        result_list = list()
        for rule in rules:
            rule = json.loads(rule['rule'])
            uid_list = self._get_point_id_list(rule, data_type)
            if len(uid_list) == 0:
                continue
            rule_data = self._apply_rule_data(uid_list, start_datetime, end_datetime,
                                              rule, query_manager, data_type)

            if rule_data is not None:
                result_list.append(rule_data)

            logger.info("query end, uid_list size: %s, start: %s, end: %s, results size: %s",
                        len(uid_list), start_datetime_str, end_datetime_str, len(result_list))
        if result_list:
            p_dataframe = pd.DataFrame(result_list)
            action_func.call(df=p_dataframe, epoch_id=end_datetime_str)

    @staticmethod
    def _apply_rule_data(uid_list,  # type: List[Tuple[str, int]]
                         start_datetime,  # type: datetime.datetime
                         end_datetime,  # type: datetime.datetime
                         rule,  # type: Dict
                         query_manager,  # type: QueryManager
                         data_type,  # type: int
                         ) -> Optional[Dict]:
        device_id = rule['assetId']
        rule_ids = rule['rules']
        start_datetime_str = date_format_str(start_datetime)

        result_list = query_manager.window_select(uid_list, start_datetime, end_datetime)
        rule_data = RuleData(device_id, rule_ids, datasource_times=start_datetime_str)
        rule_data.add_data(result_list, data_type)
        return rule_data.get_data()

    @staticmethod
    def _get_point_id_list(rule: Dict, f_data_type) -> List[Tuple[str, int]]:
        point_id = 'pointId'
        index_code = 'indexCode'
        p_list = list()
        if 'points' not in rule:
            return p_list
        for point in rule['points']:
            assert isinstance(point, dict)
            if point_id not in point:
                continue
            data_type = int(point.get('dataType', PROCESS_DATA_TYPE))
            if PROCESS_DATA_TYPE == f_data_type and data_type == f_data_type:
                p_list.append((point[point_id], data_type))
            elif INDEX_DATA_TYPE == f_data_type and index_code in point:
                # dataType: 101, 振动特征值类型，取 indexCode 特征值编码
                for index_code_value in point[index_code]:
                    p_list.append((point[point_id], int(index_code_value)))
        return p_list

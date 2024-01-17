from typing import Union, List, Iterator, Any, Callable

import ujson

from ronds_sdk import logger_config
from ronds_sdk.parser.rule_parser import EditorRuleParser
from ronds_sdk.tools import utils
from ronds_sdk.tools.constants import JsonKey
from ronds_sdk.transforms.ray.base import RayTransform

logger = logger_config.config()


class Filter(RayTransform):

    def __init__(self, filter_func=None, parallel=None, worker_index=-1):
        # type: (Callable, int, int) -> None
        super().__init__(worker_index, parallel=parallel)
        self.filter_func = filter_func

    async def process(self, inputs):
        # type: (dict[str, Union[Any, List[Any]]]) -> Iterator[Union[Any, List[Any]]]
        for input_name, input_value in inputs.items():
            if input_value is None:
                continue
            if isinstance(input_value, list):
                for split_input_value in input_value:
                    for res in self.filter(input_name, split_input_value):
                        yield res
            else:
                for res in self.filter(input_name, input_value):
                    yield res

    def filter(self, key, item):
        if self.filter_func is not None:
            self.filter_func(key, item)
        else:
            raise NotImplementedError


class FilterByPhmRules(RayTransform):

    def __init__(self,
                 rules,
                 point_id_key=None,
                 parallel=None,
                 worker_index=-1):
        # type: (list, str, int, int) -> None
        """
        按照规则进行数据的过滤, 过滤完成后, 会添加 "rg" 字段, 用来标记数据由哪条规则过滤产生
        :param worker_index:
        :param rules:
        :param point_id_key:
        """
        super().__init__(worker_index, parallel=parallel or len(rules))
        self.rules = rules
        self.point_id_key = point_id_key or JsonKey.ID.value
        self._point_groups = None

    def pre_startup(self):
        super().pre_startup()
        self._point_groups = self.init_point_groups()
        logger.info("point_groups: %s" % self._point_groups)

    def init_point_groups(self):
        """
        规则分组: 按照所需测点数据的重叠程度分组规则
        ps: 当前默认传入的规则, 已经按照使用的触点进行了分组, 直接分配分组名称

        :return:  { "point_id": [ "group_index" ] }
        """
        point_groups = dict()
        for i, rule in enumerate(self.rules):
            point_list = EditorRuleParser.point_ids(rule)
            for point in point_list:
                point_groups.setdefault(point, set()).add(i)
        return point_groups

    async def process(self, inputs):
        # type: (dict[str, Union[str, List[str]]]) -> Iterator[Union[str, List[str]]]
        for input_name, input_value in inputs.items():
            if input_value is None:
                continue
            json_obj = ujson.loads(input_value)
            if isinstance(json_obj, list):
                for json_dict in json_obj:
                    for res in self.filter(json_dict):
                        yield res
            else:
                for res in self.filter(json_obj):
                    yield res

    def filter(self, json_dict):
        # type: (dict[str, str]) -> Iterator[str]
        assert isinstance(json_dict, dict)
        point_id = json_dict[self.point_id_key]
        if point_id in self._point_groups:
            for group_index in self._point_groups.get(point_id):
                json_dict[JsonKey.RULE_GROUP.value] = group_index
                yield ujson.dumps(json_dict)
        else:
            return utils.empty_list()

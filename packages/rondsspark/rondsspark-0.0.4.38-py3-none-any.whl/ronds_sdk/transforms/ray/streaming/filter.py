import json
from typing import Union, List, Iterator, Any, Callable

import ray

from ronds_sdk.tools import utils
from ronds_sdk.tools.constants import JsonKey
from ronds_sdk.tools.utils import RuleParser
from ronds_sdk.transforms.ray.base import RayTransform


class Filter(RayTransform):

    def __init__(self, filter_func=None, parallel=None, worker_index=-1):
        # type: (Callable, int, int) -> None
        super().__init__(worker_index, parallel=parallel)
        self.filter_func = filter_func

    def process(self, inputs):
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

    def __init__(self, rules, point_id_key="id", parallel=None, worker_index=-1):
        # type: (list, str, int, int) -> None
        """
        按照规则进行数据的过滤, 过滤完成后, 会添加 "rg" 字段, 用来标记数据由哪条规则过滤产生
        :param worker_index:
        :param rules:
        :param point_id_key:
        """
        super().__init__(worker_index, parallel=parallel)
        self.rules = rules
        self.point_id_key = point_id_key
        self._point_groups = self.init_point_groups()

    def init_point_groups(self):
        """
        规则分组: 按照所需测点数据的重叠程度分组规则
        ps: 当前默认传入的规则, 已经按照使用的触点进行了分组, 直接分配分组名称

        :return:  { "point_id": [ "group_index" ] }
        """
        point_groups = dict()
        for i, rule in enumerate(self.rules):
            point_list = RuleParser.point_ids(rule)
            for point in point_list:
                if not point_groups.__contains__(point):
                    point_groups[point] = set()
                point_groups[point].add(i)
        return point_groups

    def process(self, inputs):
        # type: (dict[str, Union[str, List[str]]]) -> Iterator[Union[str, List[str]]]
        for input_name, input_value in inputs.items():
            if input_value is None:
                continue
            json_obj = json.loads(input_value)
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
        if self._point_groups.__contains__(point_id):
            for group_index in self._point_groups.get(point_id):
                json_dict[JsonKey.RULE_GROUP.value] = group_index
                yield json.dumps(json_dict)
        else:
            return utils.empty_list()



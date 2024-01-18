from typing import List

import ujson

from ronds_sdk.tools import utils
from ronds_sdk.tools.constants import JsonKey


class EditorRuleParser(object):

    def __init__(self,
                 rule_path,  # type: str
                 ):
        """
        从文件解析 phm 规则编辑器传入的规则配置信息, 用于从 Cassandra 根据指定规则读取测点数据;

        包含: 规则 id 列表, 读取的 Cassandra 数据表类型, 测点 id 列表等信息. 规则格式如下:

        [
            {
                "assetId": "3a0-xx-4f",
                "types":
                [
                    "4"
                ],
                "rules":
                [
                    "20-xx-4b"
                ],
                "points":
                [
                    {
                        "pointId": "3a-xx-19",
                        "dataType": null,
                        "measureDefId":
                        []
                    }
                ]
            }
        ]

        :param rule_path:
        """
        self._rule_path = rule_path

    def load(self) -> list:
        with open(self._rule_path, 'r', encoding='utf-8') as r:
            config = r.read()
            if config is None:
                raise RuntimeError("config is None")
            return ujson.loads(config.strip('\t\r\n'))

    @staticmethod
    def point_ids(rule: dict) -> List[str]:
        """
        读取每个 rule 配置中的测点 id list

        :param rule: 规则配置
        :return: 测点 id list
        """
        points = rule['points']
        p_list = list()
        if points:
            for point in points:
                assert isinstance(point, dict)
                if JsonKey.POINT_ID.value in point:
                    p_list.append(point[JsonKey.POINT_ID.value])
        return p_list

    @staticmethod
    def rule_ids(rule):
        # type: (dict) -> List[str]
        r_list = list()
        if JsonKey.RULES.value in rule:
            r_list = rule.get(JsonKey.RULES.value)
        return r_list

    @staticmethod
    def datetime_format():
        return utils.datetime_format()

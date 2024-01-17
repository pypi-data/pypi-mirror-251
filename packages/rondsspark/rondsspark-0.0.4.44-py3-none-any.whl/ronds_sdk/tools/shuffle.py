import random
from typing import List, Callable, Dict

import ujson

from ronds_sdk import logger_config
from ronds_sdk.tools import utils
from ronds_sdk.tools.constants import JsonKey

logger = logger_config.config()


# noinspection PyUnusedLocal
def json_hash_partitioner(json_str, shuffle_key):
    # type: (str, str) -> dict[int, List[str]]
    json_obj = ujson.loads(json_str)
    res_dict = dict()
    if isinstance(json_obj, list):
        for json_dict in json_obj:
            assert isinstance(json_dict, dict)
            # INT value will not be hash
            hash_key = utils.dict_hash(json_dict, shuffle_key)
            res_dict.setdefault(hash_key, list()).append(ujson.dumps(json_dict))
    else:
        hash_key = utils.dict_hash(json_obj, shuffle_key)
        res_dict.setdefault(hash_key, list()).append(json_str)
    return res_dict


def json_list_hash_partitioner(json_str, shuffle_key):
    # type: (str, str) -> dict[int, List[str]]
    json_obj = ujson.loads(json_str)
    res_dict = dict()
    _set_partitioner(json_obj, res_dict, shuffle_key)
    return res_dict


def _set_partitioner(json_dict, res_dict, shuffle_key):
    if JsonKey.MESSAGE.value in json_dict:
        records = json_dict[JsonKey.MESSAGE.value]
        for record in records:
            hash_key = utils.dict_hash(record, shuffle_key, int_return=True)
            res_dict.setdefault(hash_key, list()).append(record)
    for hash_key, records in res_dict.items():
        json_dict[JsonKey.MESSAGE.value] = records
        res_dict[hash_key] = [ujson.dumps(json_dict)]


# noinspection PyUnusedLocal
def single_selector(record_str: str, recv_list: List):
    """
    one single receiver partitioner
    :param record_str: record string
    :param recv_list: receiver list
    :return: selected receiver
    """
    return recv_list[0]


def random_selector(record_str: str, recv_list: List):
    """
    random partitioner
    :param record_str: record string
    :param recv_list: receiver list
    :return: selected receiver
    """
    assert record_str is not None
    return random.choice(recv_list)


def hash_selector(record_str: str, recv_list: List, key):
    """
    hash partitioner by column: $key
    :param record_str: record string
    :param recv_list: receiver list
    :param key: partition key name
    :return: selected receiver
    """
    record = ujson.loads(record_str)  # type: Dict
    hash_key = utils.dict_hash(record, key, int_return=True)

    index = hash_key % len(recv_list)
    logger.debug('key: %s, index: %d' % (hash_key, index))
    return recv_list[index]


def hash_id_selector(record_str: str, recv_list: List):
    """
    hash partitioner by column: id
    :param record_str: record string
    :param recv_list: receiver list
    :return: selected receiver
    """
    return hash_selector(record_str, recv_list, JsonKey.ID.value)


def hash_par_selector(record_str: str, recv_list: List):
    """
    hash partitioner by column: partition
    :param record_str: record string
    :param recv_list: receiver list
    :return: selected receiver
    """
    return hash_selector(record_str, recv_list, JsonKey.PARTITION.value)


def recv_selector_strategy(record_str: str, recv_list: List) -> Callable:
    """
    Generate the receiver selector strategy with the record content automatically

    Args:
        record_str (str): The record string.
        recv_list (List): The receive list.

    Returns:
        Callable: The selector strategy function.
    """

    selector = random_selector
    logger.debug("recv_selector_strategy recv_list size: %d" % len(recv_list))
    if len(recv_list) == 1:
        selector = single_selector
    else:
        record = ujson.loads(record_str)
        if JsonKey.ID.v in record:
            selector = hash_id_selector
        elif JsonKey.PARTITION.v in record:
            selector = hash_par_selector
    return selector

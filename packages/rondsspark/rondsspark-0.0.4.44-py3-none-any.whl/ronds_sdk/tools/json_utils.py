import datetime
import json
import traceback

import ujson
from numpy import ndarray

from ronds_sdk import logger_config

logger = logger_config.config()


def to_dict(value):
    if isinstance(value, datetime.datetime):
        return datetime.datetime.strftime(value, '%Y-%m-%d %H:%M:%S.%f')[0:-3]
    elif isinstance(value, ndarray):
        return value.tolist()
    else:
        return value


class JsonUtils(object):

    @staticmethod
    def dumps(obj):
        """
        Serializes an object to a JSON-formatted string using the ujson library.

        :param obj: The object to be serialized.
        :return: A JSON-formatted string representing the serialized object.
        :rtype: str
        """
        try:
            # noinspection PyArgumentList
            return ujson.dumps(obj, default=to_dict, ensure_ascii=False, escape_forward_slashes=False)
        except Exception as e:
            logger.debug("ujson.dumps failed: %s, %s" % (e, traceback.format_exc()))
            return json.dumps(obj, default=to_dict, ensure_ascii=False)

    @staticmethod
    def loads(obj):
        """ Converts JSON as string to dict object structure. """
        return ujson.loads(obj)

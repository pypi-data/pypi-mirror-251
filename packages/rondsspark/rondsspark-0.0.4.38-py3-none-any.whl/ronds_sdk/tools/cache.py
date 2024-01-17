
from cachetools import TTLCache


class ExpireCache(object):

    def __init__(self, maxsize=300, ttl=300):
        """
        包含过期时间和最大数量的缓存 Mapping
        :param maxsize:
        :param ttl:
        """
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl)

    def if_absent(self, key, value=''):
        """
        判断是否存在指定 key 的数据, 不存在则写入并返回 True
        :param key: key
        :param value: value
        :return: 不存在传入 Key 返回 True
        """
        if self.cache.__contains__(key):
            return False
        self.cache[key] = value
        return True

    def put(self, key, value):
        self.cache[key] = value

    def get(self, key):
        if self.cache.__contains__(key):
            return self.cache[key]
        return None

import redis
from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint


class RedisFilter(BaseDupeFilter):
    def __init__(self, key):
        self.conn = None
        self.key = key

    @classmethod
    def from_settings(cls, settings):
        key = settings.get("DUP_REDIS_KEY")
        return cls(key)

    def open(self):
        self.conn = redis.Redis(host="127.0.0.1", port=6379)

    def request_seen(self, request):
        fp = request_fingerprint(request)
        ret = self.conn.sadd(self.key, fp)
        return ret == 0

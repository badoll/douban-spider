import scrapy
from scrapy.spiders import Request
from crawler.items import MovieIDItem
from crawler.utils import db
from urllib.parse import urlencode
import json
from crawler.utils.logger import logger
from crawler.utils.url import get_url_values
import crawler.utils.proxy as proxy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


# 21 zone * 21 type * n (n<10000)
# https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=电影&start=0&genres=剧情&countries=中国大陆
MOVIE_LIST_API = "https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10"
MOVIE_TYPE = [
    "剧情",
    "喜剧",
    "动作",
    "爱情",
    "科幻",
    "动画",
    "悬疑",
    "惊悚",
    "恐怖",
    "犯罪",
    "同性",
    "音乐",
    "歌舞",
    "传记",
    "历史",
    "战争",
    "西部",
    "奇幻",
    "冒险",
    "灾难",
    "武侠",
]
MOVIE_ZONE = [
    "中国大陆",
    "美国",
    "香港",
    "台湾",
    "日本",
    "韩国",
    "英国",
    "法国",
    "德国",
    "意大利",
    "西班牙",
    "印度",
    "泰国",
    "俄罗斯",
    "伊朗",
    "加拿大",
    "澳大利亚",
    "爱尔兰",
    "瑞典",
    "巴西",
    "丹麦",
]


def _get_urls():
    for mzone in MOVIE_ZONE:
        for mtype in MOVIE_TYPE:
            for i in range(0, 10000, 20):
                q_val = {
                    "tags": "电影",
                    "start": i,
                    "genres": mtype,
                    "countries": mzone,
                }
                yield MOVIE_LIST_API + "&" + urlencode(q_val)


class MovieIDSpider(scrapy.Spider):
    name = "movie_id"
    allowed_domains = ["movie.douban.com"]
    db = db.cli
    logger = logger("log/{}.log".format(name))

    def start_requests(self):
        for url in _get_urls():
            if not self._have_crawled(url):
                yield Request(
                    url, callback=self.parse, errback=self.errback, dont_filter=True
                )
        # 完成所有movie_id爬取
        self._all_done()

    def parse(self, response):
        item = MovieIDItem()
        try:
            resp = json.loads(response.text)
            for m in resp["data"]:
                item["douban_id"] = m["id"]
                item["link"] = m["url"]
                item["title"] = m["title"]
                yield item
        except Exception as e:
            """
            {"msg":"检测到有异常请求从您的IP发出，请登录再试!","r":1}
            """
            self.logger.error(
                "parse response error: {}, resp: {}, url:{}, headers: {}, meta: {}".format(
                    e,
                    response.text,
                    response.url,
                    # response.request.headers,
                    "headers",
                    response.request.meta,
                )
            )
            # 删除无效代理ip，换个ip继续爬
            proxy.delete(response.request.meta["proxy"].split("//")[-1])
            yield Request(
                response.url,
                callback=self.parse,
                errback=self.errback,
                dont_filter=True,
            )

        else:
            self.logger.debug(
                "crawl succ, url:{}, headers: {}, meta: {}".format(
                    response.url,
                    # response.request.headers,
                    "headers",
                    response.request.meta,
                )
            )
            self._crawl_done(response.url)

    def errback(self, failure):
        # log all failures
        self.logger.error("errback -> {}".format(repr(failure)))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error("errback -> HttpError on {}".format(response.url))

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error("errback -> DNSLookupError on {}".format(request.url))

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error("errback -> TimeoutError on {}".format(request.url))

    # 爬取中断后重启查重
    def _have_crawled(self, url):
        query = "select url from url_to_crawl where url = %s"
        data = self.db.query_one(query, [url])
        if data is None:
            return False
        return True

    def _crawl_done(self, url):
        uv = get_url_values(url)
        _sql = (
            "insert into url_to_crawl (url,start,genres,countries) values(%s,%s,%s,%s)"
        )
        self.db.execute(_sql, [url, uv["start"], uv["genres"], uv["countries"]])

    def _all_done(self):
        _sql = "insert into url_to_crawl (url) values(%s)"
        self.db.execute(_sql, ["done"])

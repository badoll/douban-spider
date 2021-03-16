import scrapy
from scrapy.spiders import Request
from crawler.items import MovieItem
from crawler.utils import db
from crawler.utils.logger import logger
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class MovieIDSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["movie.douban.com"]
    db = db.cli
    logger = logger("log/{}.log".format(name))

    def start_requests(self):
        for url in self._get_urls():
            yield Request(
                url, callback=self.parse, errback=self.errback, dont_filter=True
            )

    def parse(self, response):
        item = MovieItem()
        item["douban_id"] = item.xph.get_douban_id(response)
        item["title"] = item.xph.get_title(response)
        item["poster"] = item.xph.get_poster(response)
        item["cate"] = item.xph.get_cate(response)
        item["director"] = item.xph.get_director(response)
        item["writer"] = item.xph.get_writer(response)
        item["performer"] = item.xph.get_performer(response)
        item["region"] = item.xph.get_region(response)
        item["language"] = item.xph.get_language(response)
        item["release_year"] = item.xph.get_release_year(response)
        item["release_date"] = item.xph.get_release_date(response)
        item["runtime"] = item.xph.get_runtime(response)
        item["rating_score"] = item.xph.get_rating_score(response)
        item["rating_num"] = item.xph.get_rating_num(response)
        item["rating_stars"] = item.xph.get_rating_stars(response)
        item["intro"] = item.xph.get_intro(response)
        item["main_cast"] = item.xph.get_main_cast(response)
        item["photos"] = item.xph.get_photos(response)
        self.logger.debug(
            "crawl succ, url:{}, headers: {}, meta: {}".format(
                response.url,
                "headers",
                response.request.meta,
            )
        )
        self._crawl_done(item["douban_id"])

        yield item

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

    def _fetch_urls(self):
        _sql = "select douban_id from movie_to_crawl where finished = 0"
        data = self.db.query(_sql)
        return tuple("https://movie.douban.com/subject/" + row[0] for row in data)

    def _get_urls(self):
        # return [
        #     "https://movie.douban.com/subject/1295644",
        #     "https://movie.douban.com/subject/3231742",
        #     "https://movie.douban.com/subject/1792928",
        #     "https://movie.douban.com/subject/1291844",
        # ]
        urls = self._fetch_urls()
        while len(urls) != 0:
            # 循环至待爬列表为空
            for url in urls:
                yield url
            urls = self._fetch_url()
        self.logger.debug("no movie to crawl for now.")

    def _crawl_done(self, douban_id):
        _sql = "update movie_to_crawl set finished = 1 where douban_id = %s"
        self.db.execute(_sql, [douban_id])

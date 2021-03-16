import scrapy
from scrapy.spiders import Request
from crawler.items import (
    NowplayingMovieItem,
    UpcomingMovieItem,
    NewReleaseMovieItem,
    WeeklyTopMovieItem,
)
from crawler.utils import db
from crawler.utils.logger import logger
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

nowplaying_url = "https://movie.douban.com/cinema/nowplaying/shenzhen"
upcoming_url = "https://movie.douban.com/cinema/later/shenzhen"
ranking_url = "https://movie.douban.com/chart"


class MovieIDSpider(scrapy.Spider):
    name = "regular"
    allowed_domains = ["movie.douban.com"]
    db = db.cli
    logger = logger("log/{}.log".format(name))

    def start_requests(self):
        yield Request(
            nowplaying_url,
            callback=self.parse_nowplaying,
            errback=self.errback,
            dont_filter=True,
        )
        yield Request(
            upcoming_url,
            callback=self.parse_upcoming,
            errback=self.errback,
            dont_filter=True,
        )
        yield Request(
            ranking_url,
            callback=self.parse_ranking,
            errback=self.errback,
            dont_filter=True,
        )

    def parse_nowplaying(self, response):
        douban_id_list = response.xpath(
            "//div[@class='article']//div[@id='nowplaying']//ul[@class='lists']/li/@id"
        ).extract()
        for douban_id in douban_id_list:
            item = NowplayingMovieItem()
            item["douban_id"] = douban_id
            yield item

        self.logger.debug(
            "crawl succ, url:{}, headers: {}, meta: {}, ids: {}".format(
                response.url, "headers", response.request.meta, douban_id_list
            )
        )

    def parse_upcoming(self, response):
        # https://movie.douban.com/subject/34458727/
        douban_id_list = list(
            i.strip("/").split("/")[-1]
            for i in response.xpath(
                "//div[@class='article']//div[@id='showing-soon']/div/a/@href"
            ).extract()
        )
        for douban_id in douban_id_list:
            item = UpcomingMovieItem()
            item["douban_id"] = douban_id
            yield item

        self.logger.debug(
            "crawl succ, url:{}, headers: {}, meta: {}, ids: {}".format(
                response.url, "headers", response.request.meta, douban_id_list
            )
        )

    def parse_ranking(self, response):
        # https://movie.douban.com/subject/34458727/
        # 新片榜
        newrelease_list = list(
            i.strip("/").split("/")[-1]
            for i in response.xpath(
                "//div[@class='article']//table//tr[@class='item']//a/@href"
            ).extract()
        )
        # 一周口碑榜
        top_list = list(
            i.strip("/").split("/")[-1]
            for i in response.xpath(
                "//div[@class='aside']/div[@id='ranking']/div[@class='movie_top']/h2[contains(text(),'一周口碑榜')]/following-sibling::ul/li//a/@href"
            ).extract()
        )
        for douban_id in newrelease_list:
            item = NewReleaseMovieItem()
            item["douban_id"] = douban_id
            yield item
        for douban_id in top_list:
            item = WeeklyTopMovieItem()
            item["douban_id"] = douban_id
            yield item

        self.logger.debug(
            "crawl succ, url:{}, headers: {}, meta: {}, ids: {}".format(
                response.url,
                "headers",
                response.request.meta,
                newrelease_list + top_list,
            )
        )

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

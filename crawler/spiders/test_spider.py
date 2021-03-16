import scrapy
import sys
import os
import pdb
from scrapy.spiders import Request


class TestSpiderSpider(scrapy.Spider):
    name = "test_spider"
    # allowed_domains = ["baidu.com"]
    # start_urls = ["http://baidu.com/", "http://baidu.com/"]
    allowed_domains = ["movie.douban.com"]
    start_urls = [
        # "https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=电影&start=0&genres=剧情&countries=中国大陆"
        "https://movie.douban.com/subject/34841067/"
    ]

    def __init__(self):
        super().__init__()
        print("path: ", sys.path)
        print("cwd: ", os.getcwd())

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse, dont_filter=False)

    def parse(self, response):
        # pdb.set_trace()
        print("response: ", response)
        print("response url: ", response.url)
        print("title: ", response.xpath("/html[@class='ua-mac ua-webkit']/body/div[@id='wrapper']/div[@id='content']/h1/span[1]").extract()[0])
        # print("request.header", response.request.headers)
        # print("request.ua", response.request.headers["User-Agent"])
        # print("request.cookie", response.request.headers["Cookie"])
        # print("request.meta", response.request.meta)

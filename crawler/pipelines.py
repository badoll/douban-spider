# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from crawler.items import (
    MovieIDItem,
    MovieItem,
    NowplayingMovieItem,
    UpcomingMovieItem,
    NewReleaseMovieItem,
    WeeklyTopMovieItem,
)
from crawler.utils import db


class CrawlerPipeline:
    db = db.cli

    def process_item(self, item, spider):
        if isinstance(item, NowplayingMovieItem):
            self._process_nowplaying_movie(item)
        elif isinstance(item, UpcomingMovieItem):
            self._process_upcoming_movie(item)
        elif isinstance(item, NewReleaseMovieItem):
            self._process_newrelease_movie(item)
        elif isinstance(item, WeeklyTopMovieItem):
            self._process_weeklytop_movie(item)
        elif isinstance(item, MovieIDItem):
            self._process_movie_id(item, "movie_to_crawl")
        elif isinstance(item, MovieItem):
            self._process_movie(item)
        return item

    def _process_movie_id(self, item, table_name):
        _sql = "INSERT INTO {} (douban_id) VALUES (%s) ON DUPLICATE KEY UPDATE douban_id = douban_id".format(
            table_name
        )
        self.db.execute(_sql, [item["douban_id"]])

    def _process_movie_id_update(self, item, table_name):
        """
        定时爬取的热映、待映、口碑电影
        """
        _sql = "INSERT INTO {} (douban_id) VALUES (%s) ON DUPLICATE KEY UPDATE finished = 0".format(
            table_name
        )
        self.db.execute(_sql, [item["douban_id"]])

    def _process_nowplaying_movie(self, item):
        self._process_movie_id_update(item, "movie_to_crawl")
        self._process_movie_id(item, "nowplaying")

    def _process_upcoming_movie(self, item):
        self._process_movie_id_update(item, "movie_to_crawl")
        self._process_movie_id(item, "upcoming")

    def _process_newrelease_movie(self, item):
        self._process_movie_id_update(item, "movie_to_crawl")
        self._process_movie_id(item, "newrelease")

    def _process_weeklytop_movie(self, item):
        self._process_movie_id_update(item, "movie_to_crawl")
        self._process_movie_id(item, "weeklytop")

    def _process_movie(self, item):
        keys = item.keys()
        values = tuple(item.values())
        fields = ",".join(keys)
        placeholder = ",".join(["%s"] * len(keys))
        _update = ",".join(
            list("{} = VALUES({})".format(i, i) for i in keys if i != "douban_id")
        )
        _sql = "INSERT INTO movie ({}) VALUES ({}) ON DUPLICATE KEY UPDATE {}".format(
            fields, placeholder, _update
        )
        self.db.execute(_sql, tuple(i.strip() for i in values))

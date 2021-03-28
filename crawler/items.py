# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
import json

DEFAULT_NULL_STR = ""
DEFAULT_NULL_NUM = "0"
MAX_INTRO_LEN = 1024


class CrawlerItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass


class MovieIDItem(Item):
    douban_id = Field()
    link = Field()
    title = Field()


class NowplayingMovieItem(MovieIDItem):
    """
    正在热映
    """

    pass


class UpcomingMovieItem(MovieIDItem):
    """
    即将上映
    """

    pass


class NewReleaseMovieItem(MovieIDItem):
    """
    新片榜
    """

    pass


class WeeklyTopMovieItem(MovieIDItem):
    """
    口碑榜
    """

    pass


class MovieXpathHelper(object):
    title = "//div[@id='content']/h1/span[@property='v:itemreviewed']/text()"
    poster = "//div[@id='mainpic']/a/img/@src"
    cate = "//div[@id='info']//span[@property='v:genre']/text()"
    director = "//div[@id='info']//span[starts-with(text(),'导演')]/following-sibling::span/a/text()"
    writer = "//div[@id='info']//span[starts-with(text(),'编剧')]/following-sibling::span/a/text()"
    performer = "//div[@id='info']//span[@class='actor']/span[@class='attrs']/a/text()"
    region = "//div[@id='info']/span[starts-with(text(),'制片国家')]/following-sibling::text()[1]"
    language = (
        "//div[@id='info']/span[starts-with(text(),'语言')]/following-sibling::text()[1]"
    )
    release_year = "//div[@id='content']/h1/span[@class='year']/text()"
    release_date = "//div[@id='info']/span[starts-with(text(),'上映日期')]/following-sibling::span[@property='v:initialReleaseDate']/text()"
    runtime = "//div[@id='info']/span[starts-with(text(),'片长')]/following-sibling::span[@property='v:runtime']/text()"
    runtime_extra = "//div[@id='info']/span[starts-with(text(),'片长')]/following-sibling::span[@property='v:runtime']/following-sibling::text()[1]"
    rating_score = "//div[@rel='v:rating']/div[@typeof='v:Rating']/strong[@property='v:average']/text()"
    rating_num = "//div[@rel='v:rating']/div[@typeof='v:Rating']//div[@class='rating_sum']//span[@property='v:votes']/text()"
    rating_stars = "//div[@rel='v:rating']/div[@class='ratings-on-weight']/div[@class='item']/span[@class='rating_per']/text()"
    intro = "//div[@class='related-info']//span[@property='v:summary']/text()"
    intro_all = "//div[@class='related-info']//span[@class='all hidden']/text()"
    main_cast_name = "//div[@id='celebrities']/ul[contains(@class,'celebrities-list')]/li/div[@class='info']/span[contains(@class,'name')]/a/text()"
    main_cast_role = "//div[@id='celebrities']/ul[contains(@class,'celebrities-list')]/li/div[@class='info']/span[contains(@class,'role')]/text()"
    main_cast_avatar = "//div[@id='celebrities']/ul[contains(@class,'celebrities-list')]/li//div[@class='avatar']/@style"
    photos_video = (
        "//div[@id='related-pic']/ul/li/a[contains(@class,'related-pic-video')]/@style"
    )
    photos = "//div[@id='related-pic']/ul/li//img/@src"

    def get_douban_id(self, response):
        return response.url.strip("/").split("/")[-1]

    def get_title(self, response):
        return response.xpath(self.title).extract_first()

    def get_poster(self, response):
        return response.xpath(self.poster).extract_first()

    def get_cate(self, response):
        return ",".join(response.xpath(self.cate).extract())

    def get_director(self, response):
        return ",".join(response.xpath(self.director).extract())

    def get_writer(self, response):
        return ",".join(response.xpath(self.writer).extract())

    def get_performer(self, response):
        return ",".join(response.xpath(self.performer).extract())

    def get_region(self, response):
        ext = "".join(response.xpath(self.region).extract()).replace(" ", "").split("/")
        return ",".join(ext)

    def get_language(self, response):
        ext = (
            "".join(response.xpath(self.language).extract()).replace(" ", "").split("/")
        )
        return ",".join(ext)

    def get_release_year(self, response):
        return (
            response.xpath(self.release_year)
            .extract_first(DEFAULT_NULL_STR)
            .strip("()")
        )

    def get_release_date(self, response):
        return ",".join(
            i.replace(",", "") for i in response.xpath(self.release_date).extract()
        )

    def get_runtime(self, response):
        runtime = list(
            i.replace(",", "") for i in response.xpath(self.runtime).extract()
        )
        # no extra: "\n        "
        # extra: "/ 153分钟(特别版) / 156分钟(终极剪辑版)" / " / 130分钟(美国)"
        extra = (
            "".join(response.xpath(self.runtime_extra).extract())
            .replace("\n", "")
            .replace(" ", "")
            .replace("\t", "")
            .replace(",", "")
        )
        if len(extra) == 0:
            return "".join(runtime)
        runtime_extra = extra.strip("/").split("/")
        return ",".join(runtime + runtime_extra)

    def get_rating_score(self, response):
        """
        评分转换为满分1000
        """
        score = float(response.xpath(self.rating_score).extract_first(DEFAULT_NULL_NUM))
        return str(round(score * 100))  # prevent precision loss

    def get_rating_num(self, response):
        return response.xpath(self.rating_num).extract_first(DEFAULT_NULL_NUM)

    def get_rating_stars(self, response):
        return ",".join(response.xpath(self.rating_stars).extract())

    def truncate_intro(self, intro):
        """
        截断过长intro
        """
        if len(intro) > MAX_INTRO_LEN:
            return intro[: MAX_INTRO_LEN - 3] + "..."
        return intro

    def get_intro(self, response):
        intro = "".join(
            i.replace("\n", "").replace(" ", "").replace("\t", "")
            for i in response.xpath(self.intro).extract()
        )
        intro_all = "".join(
            i.replace("\n", "").replace(" ", "").replace("\t", "")
            for i in response.xpath(self.intro_all).extract()
        )
        if len(intro_all) == 0:
            return self.truncate_intro(intro)
        return self.truncate_intro(intro_all)

    def get_main_cast(self, response):
        names = response.xpath(self.main_cast_name).extract()
        roles = response.xpath(self.main_cast_role).extract()
        avatars = [
            i.strip("()") for i in response.xpath(self.main_cast_avatar).re("\(.*\)")
        ]
        comb = list(
            {"name": i[0], "role": i[1], "avatar": i[2]}
            for i in zip(names, roles, avatars)
        )
        return json.dumps(comb, ensure_ascii=False)

    def get_photos(self, response):
        photos_video = [
            i.strip("()") for i in response.xpath(self.photos_video).re("\(.*\)")
        ]
        photos = response.xpath(self.photos).extract()
        return ",".join(photos_video + photos)


class MovieItem(Item):
    douban_id = Field()
    title = Field()
    poster = Field()
    cate = Field()
    director = Field()
    writer = Field()
    performer = Field()
    region = Field()
    language = Field()
    release_year = Field()
    release_date = Field()
    runtime = Field()
    rating_score = Field()
    rating_num = Field()
    rating_stars = Field()
    intro = Field()
    main_cast = Field()
    photos = Field()
    xph = MovieXpathHelper()

    def check_ok(self):
        if self["title"] is None or len(self["title"]) == 0:
            return False
        return True


if __name__ == "__main__":
    pass

import json
from mock_movie_data import mock_data, nowplaying_data
from scrapy.selector import Selector
import sys
sys.path.append(".")
from crawler.items import MovieXpathHelper as dxp


def test_id_api():
    data = """{"data":[{"directors":["宁海强"],"rate":"4.6","cover_x":1500,"star":"25","title":"歼十出击","url":"https:\/\/movie.douban.com\/subject\/3778238\/","casts":["王斑","李光洁","黄奕","胡可","祝新运"],"cover":"https://img3.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p936656881.webp","id":"3778238","cover_y":2100},{"directors":["彭小莲"],"rate":"7.5","cover_x":500,"star":"40","title":"美丽上海","url":"https:\/\/movie.douban.com\/subject\/1422040\/","casts":["王祖贤","郑振瑶","冯远征","顾美华","娜仁花"],"cover":"https://img9.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p498333714.webp","id":"1422040","cover_y":714},{"directors":["宋川"],"rate":"4.7","cover_x":2339,"star":"25","title":"巧巧","url":"https:\/\/movie.douban.com\/subject\/26430195\/","casts":["梁雪芹","章宇","周铨"],"cover":"https://img9.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2422955016.webp","id":"26430195","cover_y":3312},{"directors":["吴林"],"rate":"5.0","cover_x":1417,"star":"25","title":"爱别离","url":"https:\/\/movie.douban.com\/subject\/21264285\/","casts":["张檬","黄阅","王盈凯","卓予童","缪婷茹"],"cover":"https://img1.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2132358869.webp","id":"21264285","cover_y":1980},{"directors":["彭磊"],"rate":"6.7","cover_x":805,"star":"35","title":"乐队","url":"https:\/\/movie.douban.com\/subject\/6560928\/","casts":["赵怡文","江雨晨","朱筱毅","庞宽","健崔"],"cover":"https://img9.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p1494950336.webp","id":"6560928","cover_y":1111},{"directors":["胡国瀚"],"rate":"6.0","cover_x":1080,"star":"30","title":"缉妖法海传","url":"https:\/\/movie.douban.com\/subject\/30276392\/","casts":["黄蓉","白宇","姜震昊","乔曦","吴宥萱"],"cover":"https://img9.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2529213934.webp","id":"30276392","cover_y":1920},{"directors":["熊欣欣"],"rate":"3.8","cover_x":945,"star":"20","title":"战·无双","url":"https:\/\/movie.douban.com\/subject\/3596509\/","casts":["蒋璐霞","李灿森","张兆辉","利沙华","迈克·莫勒"],"cover":"https://img3.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2246997981.webp","id":"3596509","cover_y":1390},{"directors":["王珈","沈东"],"rate":"6.5","cover_x":800,"star":"35","title":"惊天动地","url":"https:\/\/movie.douban.com\/subject\/3987383\/","casts":["侯勇","李幼斌","童蕾","岳红","巫刚"],"cover":"https://img1.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p1378642318.webp","id":"3987383","cover_y":1176},{"directors":["万玛才旦"],"rate":"8.2","cover_x":679,"star":"40","title":"静静的嘛呢石","url":"https:\/\/movie.douban.com\/subject\/1756057\/","casts":["洛桑丹派","确赛","巨焕仓活佛","三木旦","普日哇"],"cover":"https://img1.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2159479357.webp","id":"1756057","cover_y":960},{"directors":["阿牛","赵宇","陈立谦"],"rate":"3.3","cover_x":4843,"star":"15","title":"半熟少女","url":"https:\/\/movie.douban.com\/subject\/26345159\/","casts":["黄灿灿","敖犬","南笙","王子豪","王子杰"],"cover":"https://img2.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2326378603.webp","id":"26345159","cover_y":6969},{"directors":["谢飞"],"rate":"8.0","cover_x":496,"star":"40","title":"湘女萧萧","url":"https:\/\/movie.douban.com\/subject\/1434275\/","casts":["娜仁花","邓晓光","管宗祥","张瑜","贾大中"],"cover":"https://img9.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2215972216.webp","id":"1434275","cover_y":684},{"directors":["郭宝昌"],"rate":"9.2","cover_x":405,"star":"45","title":"大宅门","url":"https:\/\/movie.douban.com\/subject\/5301572\/","casts":["斯琴高娃"],"cover":"https://img9.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p1964425586.webp","id":"5301572","cover_y":575},{"directors":["蔡楚生"],"rate":"8.4","cover_x":3071,"star":"40","title":"新女性","url":"https:\/\/movie.douban.com\/subject\/1421676\/","casts":["阮玲玉","郑君里","费柏青","吴茵","洪警铃"],"cover":"https://img9.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2246439495.webp","id":"1421676","cover_y":4346},{"directors":["陈卓"],"rate":"7.0","cover_x":5250,"star":"35","title":"杨梅洲","url":"https:\/\/movie.douban.com\/subject\/10480963\/","casts":["李强","尹雅宁","吴冰滨","余宣"],"cover":"https://img9.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p1650336686.webp","id":"10480963","cover_y":7874},{"directors":["靳夕"],"rate":"8.9","cover_x":500,"star":"45","title":"西岳奇童","url":"https:\/\/movie.douban.com\/subject\/1466114\/","casts":["乔榛","丁建华"],"cover":"https://img1.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2407038217.webp","id":"1466114","cover_y":707},{"directors":["江涛"],"rate":"6.7","cover_x":2127,"star":"35","title":"无底洞","url":"https:\/\/movie.douban.com\/subject\/6087768\/","casts":["沙溢","瞿颖","叶青","吴卫东","王伟源"],"cover":"https://img2.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p1035452422.webp","id":"6087768","cover_y":3119},{"directors":["朱延平"],"rate":"6.2","cover_x":580,"star":"30","title":"恋爱大赢家","url":"https:\/\/movie.douban.com\/subject\/2080707\/","casts":["许绍洋","杨恭如","刘亦菲","林志颖","陈子强"],"cover":"https://img9.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2354941225.webp","id":"2080707","cover_y":902},{"directors":["谭华"],"rate":"4.7","cover_x":714,"star":"25","title":"摇滚英雄","url":"https:\/\/movie.douban.com\/subject\/25706778\/","casts":["秦昊","李梦","刘雅瑟","都日昭日格图","马恺曼"],"cover":"https://img9.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2250588156.webp","id":"25706778","cover_y":1000},{"directors":["安佳星"],"rate":"7.0","cover_x":2480,"star":"35","title":"老大不小","url":"https:\/\/movie.douban.com\/subject\/34913597\/","casts":["高炜","杨长青","赵燕国彰","王睿","戴菲"],"cover":"https://img2.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2612798743.webp","id":"34913597","cover_y":3472},{"directors":["刘畅"],"rate":"3.8","cover_x":1000,"star":"20","title":"二十岁","url":"https:\/\/movie.douban.com\/subject\/26756259\/","casts":["屈楚萧","孔垂楠","叶子诚","于文文","徐晓璐"],"cover":"https://img9.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2541193765.webp","id":"26756259","cover_y":1400}]}"""
    data2 = """ {"data":[]} """
    resp = json.loads(data)
    for m in resp["data"]:
        print(m["title"], m["url"], m["id"])


def print_attr(name, value):
    print(name, value, "", sep="|")


def test_parse_movie_data():
    sel = Selector(text=mock_data)
    print_attr(
        "title",
        sel.xpath(dxp.title).extract_first(),
    )
    print_attr(
        "poster",
        sel.xpath(dxp.poster).extract_first(),
    )
    print_attr(
        "cate",
        sel.xpath(dxp.cate).extract(),
    )
    print_attr(
        "director",
        sel.xpath(dxp.director).extract(),
    )
    print_attr(
        "writer",
        sel.xpath(dxp.writer).extract(),
    )
    print_attr(
        "performer",
        sel.xpath(dxp.performer).extract(),
    )
    print_attr(
        "region",
        "".join(sel.xpath(dxp.region).extract()).replace(" ", "").split("/"),
    )
    print_attr(
        "language",
        "".join(sel.xpath(dxp.language).extract()).replace(" ", "").split("/"),
    )
    print_attr(
        "release_year",
        sel.xpath(dxp.release_year).extract_first().strip("()"),
    )
    print_attr(
        "release_date",
        sel.xpath(dxp.release_date).extract(),
    )
    print_attr(
        "runtime",
        sel.xpath(dxp.runtime).extract(),
    )
    print_attr(
        "runtime_extra",
        "".join(sel.xpath(dxp.runtime_extra).extract())
        .replace("\n", "")
        .replace(" ", "")
        .strip("/")
        .split("/"),
    )
    print_attr(
        "rating_score",
        sel.xpath(dxp.rating_score).extract(),
    )
    print_attr(
        "rating_num",
        sel.xpath(dxp.rating_num).extract(),
    )
    print_attr(
        "rating_stars",
        sel.xpath(dxp.rating_stars).extract(),
    )
    print_attr(
        "intro",
        "".join(i.replace("\n", "").strip() for i in sel.xpath(dxp.intro).extract()),
    )
    print_attr(
        "intro_all",
        "".join(
            i.replace("\n", "").strip() for i in sel.xpath(dxp.intro_all).extract()
        ),
    )
    print_attr(
        "main_cast_name",
        sel.xpath(dxp.main_cast_name).extract(),
    )
    print_attr(
        "main_cast_role",
        sel.xpath(dxp.main_cast_role).extract(),
    )
    print_attr(
        "main_cast_avatar",
        [i.strip("()") for i in sel.xpath(dxp.main_cast_avatar).re("\(.*\)")],
    )
    print_attr(
        "photos_video",
        [i.strip("()") for i in sel.xpath(dxp.photos_video).re("\(.*\)")],
    )
    print_attr(
        "photos",
        sel.xpath(dxp.photos).extract(),
    )


def test_nowplying():
    sel = Selector(text=nowplaying_data)
    print_attr(
        "douban_id_list",
        sel.xpath("//div[@class='article']//div[@id='nowplaying']//ul[@class='lists']/li/@id").extract()
    )

if __name__ == "__main__":
    # test_id_api()
    # test_parse_movie_data()
    test_nowplying()
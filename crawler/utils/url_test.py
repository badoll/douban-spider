from url import *

MOVIE_LIST_API = "https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10"
url = "https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=0&genres=%E5%89%A7%E6%83%85&countries=%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86"


def test_encode():
    q_val = {"tags": "电影", "start": 0, "genres": "剧情", "countries": "中国大陆"}
    u = MOVIE_LIST_API + "&" + urlencode(q_val)
    print(url == u)


def test_decode():
    print(parse_qsl(urlsplit(url).query))
    print(dict(parse_qsl(urlsplit(url).query)))


if __name__ == "__main__":
    test_decode()

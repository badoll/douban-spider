from urllib.parse import urlencode, parse_qsl, urlsplit


def get_url_values(url):
    return dict(parse_qsl(urlsplit(url).query))

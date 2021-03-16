import requests
import json
import time
from crawler.utils.logger import dur_logger


def get():
    # start = time.time()
    resp = requests.get("http://127.0.0.1:5010/get/").text
    result = json.loads(resp)
    # dur_logger.debug("get proxy dur: {}".format(time.time() - start))
    return result["proxy"]


def delete(proxy):
    # start = time.time()
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
    # dur_logger.debug("del proxy dur: {}".format(time.time() - start))

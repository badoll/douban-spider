import pymysql
import yaml
from crawler.utils.logger import logger


class _DB(object):
    logger = logger("log/db.log")

    def __init__(self, conf_file):
        with open(conf_file, "r", encoding="utf-8") as fy:
            conf = yaml.load(fy, yaml.SafeLoader)
            self.conn = pymysql.connect(
                host=conf["HOST"],
                port=conf["PORT"],
                user=conf["USER"],
                password=conf["PWD"],
                db=conf["DB"],
                charset=conf["CHARSET"],
            )
            self.cur = self.conn.cursor()

    def execute(self, sql, args=None):
        try:
            self.cur.execute(sql, args)
        except Exception as e:
            self.conn.rollback()
            self.logger.error(
                "sql execute error: {}, sql: {}, args: ({})".format(e, sql, args)
            )
        else:
            # self.logger.debug("sql execute succ, sql: {}, args: ({})".format(sql, args))
            self.conn.commit()

    def query_one(self, sql, args=None):
        self.cur.execute(sql, args)
        return self.cur.fetchone()

    def query(self, sql, args=None):
        self.cur.execute(sql, args)
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()

    def _crawl_done(self, url):
        _sql = "insert into url_to_crawl values(%s)"
        self.execute(_sql, [url])


cli = _DB("conf/db/mysql.yaml")

if __name__ == "__main__":
    db = _DB("conf/db/mysql.yaml")
    data = db.query("select url from url_to_crawl where url = %s", ["test_1url"])
    print(data, type(data))
    print(len(data))
    print(data is None)
    data = db.query_one("select url from url_to_crawl where url = %s", ["test_1url"])
    print(data, type(data))
    print(data is None)
    db._crawl_done("test_url2")

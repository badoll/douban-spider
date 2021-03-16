import yaml
from crawler.singleton import singleton

_LOG_CONF_FILE = "conf/log/conf.yaml"


# def _get_log_conf_file():
#     # ../../conf
#     return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@singleton
class GConfig:
    log_cfg = {}
    init_fail = False

    def init_conf(self):
        try:
            self._init_log_conf()
        except Exception as e:
            self.init_fail = True
            print("get error: ", e)

    def _init_log_conf(self):
        with open(_LOG_CONF_FILE, "r", encoding="utf-8") as fy:
            self.log_cfg = yaml.load(fy, yaml.SafeLoader)

    def get_log_cfg(self, key):
        if self.init_fail:
            return ""
        return self.log_cfg[key]


g_conf = GConfig()

if __name__ == "__main__":
    c = GConfig()
    c2 = GConfig()
    print(id(c) == id(c2))

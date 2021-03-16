import loguru
import yaml


class logger(loguru._Logger):
    def __init__(self, log_file, conf_file="conf/log/conf.yaml"):
        super(logger, self).__init__(
            loguru._Core(), None, 0, False, False, False, False, True, None, {}
        )
        with open(conf_file, "r", encoding="utf-8") as fy:
            log_cfg = yaml.load(fy, yaml.SafeLoader)
            self.add(
                log_file,
                level=log_cfg["Log_Level"],
                format=log_cfg["Log_Format"],
                rotation=log_cfg["Log_Rotation"],
                retention=log_cfg["Log_Retention"],
                encoding=log_cfg["Log_Encoding"],
            )


dur_logger = logger("log/dur.log")

import logging
import colorlog
from base.conf_obtain import sys_config


class LogServer:
    LogColorMap = {
        'INFO': 'white',
        'DEBUG': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }

    FILE_DIR = sys_config.file_dir
    FILE_LEVEL = sys_config.file_level
    STREAM_LEVEL = sys_config.stream_level
    OUT_PUT = sys_config.out_put

    def __init__(self, name, filename=FILE_DIR, out_put=OUT_PUT, file_level=FILE_LEVEL, stream_level=STREAM_LEVEL):
        self.filename = filename
        self.out_put = out_put
        self.file_level = file_level
        self.stream_level = stream_level
        self.name = name
        self.log_init()

    def log_init(self):
        self.logger = logging.getLogger(self.name)
        self.sh = logging.StreamHandler()
        self.fh = logging.FileHandler(filename=self.filename, mode='a', encoding='utf-8')
        self.fmt = logging.Formatter("[%(asctime)s] - [(%(name)s)][%(levelname)s]>>>%(message)s")
        self.cfmt = colorlog.ColoredFormatter("%(log_color)s[%(asctime)s] - [(%(name)s)][%(levelname)s]>>>%(message)s",
                                              datefmt='%Y-%m-%d  %H:%M:%S',
                                              log_colors=self.LogColorMap)  # 默认为白色
        self.logger.setLevel(logging.getLevelName(self.file_level))
        self.sh.setLevel(logging.getLevelName(self.stream_level))
        self.sh.setFormatter(self.cfmt)
        self.fh.setFormatter(self.fmt)
        if self.out_put:
            self.logger.addHandler(self.sh)
        self.logger.addHandler(self.fh)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

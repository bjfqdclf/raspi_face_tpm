import logging
import colorlog


class LogServer:
    LogColorMap = {
        'INFO': 'white',
        'DEBUG': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }

    def __init__(self, name, filename="sys.log", out_put=True, file_level='DEBUG', stream_level='DEBUG'):
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

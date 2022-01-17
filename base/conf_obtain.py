import os
from configparser import ConfigParser


class SysConfig:
    # 读取配置文件
    conf_exit = False
    conf_name = "../school_sys.conf"
    # while conf_exit is False:
    if os.path.exists(conf_name):  # 在项目根目录下启动时读取conf文件
        conf_name = conf_name
        conf_exit = True
        # conf_name = "../" + conf_name
    if conf_exit:
        try:
            conf = ConfigParser()
            conf.read(conf_name, encoding="utf-8")
            # 读取设备信息
            device_id = conf.get("device_info", "device_id")
            # 读取TX_API配置
            SecretId = conf.get("tx_api", "secret_id")
            SecretKey = conf.get("tx_api", "secret_key")
            # 读取database配置
            db_name = conf.get("database", "db_name")
            db_user = conf.get("database", "db_username")
            db_password = conf.get("database", "db_password")
            db_addr = conf.get("database", "db_addr")
            db_port = int(conf.get("database", "db_port"))
            # 读取log配置
            file_dir = conf.get("log", "file_dir", fallback="../face_sys_log.log")
            file_level = conf.get("log", "file_level", fallback="DEBUG")
            stream_level = conf.get("log", "stream_level", fallback="DEBUG")
            out_put = conf.get("log", "out_put", fallback=True)
            # 读取测温配置
            measure_parts = int(conf.get("temp", "measure_parts", fallback=1))  # 0：额温    1：腕温
            distance_compensation = conf.get("temp", "distance_compensation", fallback=False)

        except KeyError as e:
            pass

    @classmethod
    def update(cls, section, key, value):
        conf = ConfigParser()
        conf.read(cls.conf_name)
        print("update cfg file:", cls.conf_name)
        conf.set(section, key, value)
        conf.write(open(cls.conf_name, 'w'))


sys_config = SysConfig()

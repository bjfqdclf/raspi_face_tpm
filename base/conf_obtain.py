import os

from configparser import ConfigParser
# from utils.parse import parse

class SysConfig:
    # 读取配置文件
    conf_exit = False
    conf_name = "school_sys.conf"
    if os.path.exists(conf_name):  # 在项目根目录下启动时读取conf文件
        conf_name = conf_name
        conf_exit = True
    if conf_exit:
        try:
            conf = ConfigParser()
            conf.read(conf_name, encoding="utf-8")
            # 读取TX_API配置
            SecretId = conf.get("tx_api", "secret_id")
            SecretKey = conf.get("tx_api", "secret_key")



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
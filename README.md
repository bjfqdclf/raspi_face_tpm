# 1 概况

## 1.1 运行环境

- ubuntu20.04_arm
- python3.9.7

## 1.2 硬件

- 树莓派4
- 摄像头 OV5647
- 红外测温 MLX90614ESF-BBA
- 超声波距离感应器 HC-SR04
- 触摸屏

## 1.3 开发工具

- pycharm
- git
- postman
- naivcat

# 2 基础配置

## 2.1 文件目录设置

- base
    - conf_obtain.py
    - db_server.py
    - log_server.py
    - start.py
    - sys_math_interface.py
- distance_measure
    - distance_dirver_model.py
- face_recognition
    - img
    - classifier_file
    - face_detect.py
    - face_search.py
    - img_obtain.py
- tem_measure
    - temp_comp_model.py
    - temp_driver_model.py
- school_sys.conf

## 2.2 配置文件

```
[device_info]
device_id = 001  # 设备唯一编码

[database]
db_addr = 127.0.0.1  # 数据库地址
db_port = 3456  # 数据端口
db_database = school_sys  # 数据库库名
db_username = name  # 数据库用户名
db_password = pwd  # 数据库密码

[tx_api]
# 腾讯人员库API
secret_id = 111
secret_key = 111

[log]
file_name = /home/face_sys_log.log  # log文件地址
out_put = True  # 是否打开终端输出
file_level = DEBUG  # log文件等级
stream_level = DEBUG  # log终端输出等级

[temp]
measure_parts = 1  # 测量方式：0-额温、1-腕温
distance_compensation = False   # 距离补偿 需要有超声波传感器
```

# 3 基础功能实现

## 3.1 基础架构功能实现

### 3.1.1 配置文件读取

> 配置文件原则上需放在项目根目录下，根据文件名匹配。
> 

### 3.1.1.1 模板配置文件

- school_sys.conf.example

> 模板配置文件为未填参数或填写示例参数的配置文件，使用时可将模板文件复制并补全，删除文件后缀(.example)即可生效。
> 

### 3.1.1.2 配置文件读取流程图

![配置文件读取](https://user-images.githubusercontent.com/45928505/168596772-4b65f4da-b28b-481e-8592-2fa719aa785a.png)

### 3.1.1.3 配置文件读取实现

- 使用库
    - os
    - ConfigParser
- 实现代码

```
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
            device_id = int(conf.get("device_info", "device_id"))
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
```

### 3.1.2 log日志输出

### 3.1.2.1 log日志输出服务

- 使用库
    - logging
    - color_log

> log文件服务可在其他服务调用打印，通过配置文件可自定义log文件存放位置、是否开启终端输出、终端or文件输出log文件等级。并通过重写logging库的log等级方法实现外部服务调用。
> 

### 3.1.2.2 log日志输出等级

1. info
2. debug
3. warning
4. error
5. critical

### 3.1.2.3 流程图
![log输出](https://user-images.githubusercontent.com/45928505/168596894-e6b0392a-9a09-485a-918c-cc98f421df80.jpg)



### 3.1.2.4 代码实现

```
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
```

### 3.1.3 数据库连接

### 3.1.3.1 数据库连接服务

- 使用库
    - pymysql == 1.0.2
    - datetime

> 数据库连接服务通过读取配置文件中配置的数据库地址、端口、用户名、密码、库名等信息连接对应的数据库。此接口还提供一些数据库快捷操作的相关方法。
> 

### 3.1.3.2 流程图
![数据库连接](https://user-images.githubusercontent.com/45928505/168596941-53a6280e-7a0a-40d6-ad98-678bdbea29c5.jpg)


### 3.1.3.3 代码实现

```
import pymysql
from base.conf_obtain import sys_config
from base.log_server import LogServer
import datetime

class DatabaseServer:
    log = LogServer("DatabaseServer")

    def __init__(self):
        self.cursor = None
        self.db = None
        self.host = sys_config.db_addr
        self.port = sys_config.db_port
        self.user = sys_config.db_user
        self.password = sys_config.db_password
        self.database = sys_config.db_name

        self.db_connect()

    def db_connect(self):
        try:
            self.db = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database)
            self.cursor = self.db.cursor()
            self.log.info("数据库连接成功")
        except Exception as err:
            self.log.error(err)
            self.log.debug('数据库未连接')

  def db_close(self):
      self.db.close()
```

```
@staticmethod
def db_datetime():
    """
    生成与sql的datetime格式匹配的当前时间
    """
    time = str(datetime.datetime.now()).split('.')[0]
    time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    # time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return time

def db_execute(self, sql):
    try:
        self.cursor.execute(sql)
        self.db.commit()
    except Exception as err:
        self.log.error(err)
        self.db.rollback()
    else:
        self.log.info(f"{sql} 数据插入成功")
```

## 3.2 主体功能实现
### 3.2.1 人脸识别流程
![raspi系统主架构](https://user-images.githubusercontent.com/45928505/168597107-27b29319-ea4f-41e3-a083-a8b8b5ebdd7c.jpg)

### 3.2.2 红外测温

- 硬件型号：MLX90614ESF-BBA
- 主要服务：
    - temp_dirver_model.py 红外测温硬件驱动服务
    - temp_comp_model.py 温度补偿服务

> 红外测温服务可以通过python加载硬件通过IIC接口连接的红外测温传感器的数据。
> 

> 温度补偿服务通过验证的温度对应关系，提供腕温转换成额温、利用超声波测距服务进行温度距离补偿。
>

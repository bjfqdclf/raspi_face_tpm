import pymysql
from base.conf_obtain import sys_config
from base.log_server import LogServer


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
            print(err)

    def db_execute(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as err:
            self.log.error(err)
            self.db.rollback()
        else:
            self.log.info(f"{sql} 数据插入成功")

    def db_close(self):
        self.db.close()


db_server = DatabaseServer()

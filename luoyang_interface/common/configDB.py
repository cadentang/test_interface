import pymysql
import common.readConfig as readConfig
from common.log import MyLog as Log

localReadConfig = readConfig.ReadConfig()

class MyDB:
    global host, username, password, port, database, config
    host = localReadConfig.get_db('host')
    username = localReadConfig.get_db('username')
    password = localReadConfig.get_db('password')
    port = localReadConfig.get_db('port')
    database = localReadConfig.get_db('database')
    config = {
        'host': str(host),
        'user': username,
        'password': password,
        'port': int(port),
        'db': database
    }

    def __init__(self):
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.db = None
        self.cursor = None

    def connectDB(self):
        """
        连接数据库
        :return: 
        """
        try:
            # connect to db
            self.db = pymysql.connect(**config)
            # create cursor
            self.cursor = self.db.cursor()
            print("Connect DB successfully!")
        except ConnectionError as ex:
            self.logger.error(str(ex))

    def executeSQL(self, sql, params):
        """
        execute sql
        :param sql: 
        :param params: 
        :return: 
        """
        self.connectDB()
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor

    def get_all(self, cursor):
        """
        得到所有执行sql后的结果
        :param cursor: 
        :return: 
        """
        value = cursor.fetchall()
        return value

    def get_one(self, cursor):
        """
        得到一条sql语句执行结果
        :param cursor: 
        :return: 
        """
        value = cursor.fetchone()
        return value

    def closeDB(self):
        """
        关闭数据库连接
        :return: 
        """

        self.db.close()
        print("database closed!")
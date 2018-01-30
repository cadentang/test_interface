import os
import codecs
import configparser
"""
:os-操作系统处理模块，
:codecs-自然语言编码转换模块
:configparser-读写配置文件模块
"""
proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "config.ini")
print(configPath)


# 读取配置文件
class ReadConfig:
    def __init__(self):
        fd = open(configPath, 'rb')
        data = fd.read()
        # 删除带有BOM信息的UTF-8文件的前三字节
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, 'w')
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_headers(self, name):
        value = self.cf.get("HEADERS", name)
        return value

    def set_headers(self, name, value):
        self.cf.set("HEADERS", name, value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)

    def get_url(self, name):
        value = self.cf.get("URL", name)
        return value

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value

if __name__ == '__main__':
    f = ReadConfig()
    print(f.get_db('host'))


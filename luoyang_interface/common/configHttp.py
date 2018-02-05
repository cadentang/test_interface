import requests
import common.readConfig as readConfig
from common.log import MyLog
import json

localReadConfig = readConfig.ReadConfig()


class ConfigHttp:

    def __init__(self):
        global scheme, host, port, timeout
        scheme = localReadConfig.get_http("scheme")
        host = localReadConfig.get_http("baseurl")
        port = localReadConfig.get_http("port")
        timeout = localReadConfig.get_http("timeout")
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.files = {}
        self.state = 0

    def set_url(self, url):
        """
        得到接口url
        :param url: 接口url
        :return: 
        """
        self.url = scheme + "://" + host + url

    def set_headers(self, header):
        """
        设置头信息
        :param header: 
        :return: 
        """
        self.headers = header

    def set_data(self, data):
        """
        
        :param data: 
        :return: 
        """
        self.data = data

    def set_files(self, filename):
        """
        set upload files
        :param filename: 
        :return: 
        """
        if filename != '':
            file_path = 'F:/AppTest/Test/interfaceTest/testFile/img/' + filename
            self.files = {'file': open(file_path, 'rb')}

        if filename == '' or filename is None:
            self.state = 1

    # http get方法
    def get(self):
        try:
            resposnse = requests.get(self.url, headers=self.headers, params=self.params,timeout=float(timeout))
            return resposnse
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # post方法，不包括上传附件
    def post(self):
        """
        post方法
        :return: 
        """
        try:
            response = requests.post(self.url, headers=self.headers,
                                     params=self.params, data=self.data,
                                     timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # post方法，包括上传附件
    def postWithJson(self):
        """
        上传
        :return: 
        """
        try:
            response = requests.post(self.url, headers=self.headers,
                                     json=self.data, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

if __name__ == "__main__":
    print("ConfigHTTP")





import unittest
import paramunittest
import common.readConfig as readConfig
from common import log as Log
from common import public
from common import configHttp as configHttp

localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
localLogin_xls = public.get_xls("userCase.xlsx", "login")
localAccountSetting_xls = public.get_xls("userCase.xls", "accountSetting")


@paramunittest.parametrized(*localAccountSetting_xls)
class AccountSetting(unittest.TestCase):

    def setParameters(self, case_name, method, token, sex, telephone, nickname, birthday, country_id, result,code, msg):
        """
        从Excel中获取接口的参数，每列代表一个参数
        :param case_name: 
        :param method: 
        :param token: 
        :param sex: 
        :param telephone: 
        :param nickname: 
        :param birthday: 
        :param country_id: 
        :param result: 
        :param code: 
        :param msg: 
        :return: 
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.sex = str(sex)
        self.telephone = str(telephone)
        self.nickname = str(nickname)
        self.birthday = str(birthday)
        self.countryId = str(country_id)
        self.result = str(result)
        self.code = str(code)
        self.msg = str(msg)
        self.response = None
        self.info = None
        self.login_token = None

    def description(self):
        """
        
        :return: 
        """
        return self.case_name

    def setUp(self):
        """
        
        :return: 
        """
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        # login
        self.login_token

    def testAccountSetting(self):
        """
        测试用例
        :return: 
        """
        self.url = public.get_url_from_xml("accountSetting")
        localConfigHttp.set_url(self.url)

        # set header
        if self.token == '0':
            token = self.login_token
        else:
            token = self.token
        header = {'token': token}
        localConfigHttp.set_headers(header)

        # set param
        data = {'sex': self.sex,
                'telephone': self.telephone,
                'nickname': self.nickname,
                'birthday': self.birthday,
                'country_id': self.countryId}
        localConfigHttp.set_data(data)

        # test interface
        self.response = localConfigHttp.post()
        # check result
        self.checkResult()

    def tearDown(self):
        """
        
        :return: 
        """
        # logout
        businessCommon.logout(self.login_token)
        self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])

    def checkResult(self):
        self.info = self.response.json()
        public.show_return_msg(self.response)

        if self.result == '0':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
            result = self.info['info'].get('result')
            self.assertEqual(result, 1)

        if self.result == '1':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)






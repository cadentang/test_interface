import requests
import common.readConfig as readConfig
import os
from xlrd import open_workbook
from xml.etree import ElementTree
from common import configHttp
from common.log import MyLog as Log
import json

localReadConfig = readConfig.ReadConfig()
proDir = readConfig.proDir
localConfigHttp = configHttp.ConfigHttp()
log = Log.get_log()
logger = log.get_logger()

caseNo = 0


def get_visitor_token():
    """
    得到token，以后的接口访问每次都会带上它
    :return: 
    """
    host = localReadConfig.get_http("BASEURL")
    response = requests.get(host + '/pages/AppLogin/login')
    info = response.json()
    token = info.get("info")
    logger.debug("Create token:%s" % (token))
    return token


def set_visitor_token_to_config():
    """
    
    :return: 
    """
    token_v = get_visitor_token()
    localReadConfig.set_headers("TOKEN_V", token_v)


def get_value_from_return_json(json, name1, name2):
    """
    通过键得到值
    :param json: 
    :param name1: 
    :param name2: 
    :return: 
    """
    info = json['info']
    group = info[name1]
    value = group[name2]
    return value


def show_return_msg(response):
    """
    
    :param response: 
    :return: 
    """
    url = response.url
    msg = response.text
    print("\n请求地址：" + url)
    print("\n请求返回值：" + '\n' + json.dumps(json.loads(msg),
                                         ensure_ascii=False,sort_keys=True, indent=4))

# *********read testcase excel**********
def get_xls(xls_name, sheet_name):
      
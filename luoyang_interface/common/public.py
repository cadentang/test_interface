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
proDir = os.path.dirname(proDir)
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
    """
    从excel文件中得到接口数据
    :param xls_name: Excel文件名
    :param sheet_name: sheet页名
    :return: 
    """
    cls = []
    xlspath = os.path.join(proDir, 'testFile', 'case', xls_name)
    file = open_workbook(xlspath)
    sheet = file.sheet_by_name(sheet_name)
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    return cls

# **************** read sql from xml ****************
database = {}


def set_xml():
    """
    
    :return: 
    """
    if len(database) == 0:
        sql_path = os.path.join(proDir, 'testFile', 'SQL.xml')
        tree = ElementTree.parse(sql_path)
        for db in tree.findall("database"):
            db_name = db.get("name")
            print(db_name)
            table = {}
            for tb in db.getchildren():
                table_name = tb.get("name")
                print(table_name)
                sql = {}
                for data in tb.getchildren():
                    sql_id = data.get("id")
                    print(sql_id)
                    sql[sql_id] = data.text
                table[table_name] = sql
            database[db_name] = table


def get_xml_dict(database_name, table_name):
    """
    
    :param database_name: 
    :param table_name: 
    :return: 
    """
    set_xml()
    database_dict = database.get(database_name).get(table_name)
    return database_dict


def get_sql(database_name, table_name, sql_id):
    """
    通过名称和sql语句ID获得sql
    :param database_name: 数据库名称
    :param table_name: 表名
    :param sql_id: sql语句ID
    :return: 返回查询的sql语句
    """
    db = get_xml_dict(database_name, table_name)
    sql = db.get(sql_id)
    return sql


# ***************** read interfaseURL xml ****************
def get_url_from_xml(name):
    """
    从interfaceURL.xml中获取接口url
    :param name: 
    :return: url
    """
    url_list = []
    url_path = os.path.join(proDir, 'testFile', 'interfaceURL.xml')
    tree = ElementTree.parse(url_path)
    for u in tree.findall('url'):
        url_name = u.get('name')
        if url_name == name:
            for c in u.getchildren():
                url_list.append(c.text)
    url = '/v2/' + '/'.join(url_list)
    return url


# ***************** read url.json xml ****************
def get_url_from_json(name):
    """
    从url.json中获取接口url
    :param name: 文件名
    :return:  
    """

if __name__ == "__main__":
    print(get_xls("userCase.xlsx", "login"))
    set_visitor_token_to_config()


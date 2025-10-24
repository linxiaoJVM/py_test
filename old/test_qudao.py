# -*- coding:utf-8 -*-
import requests
import datetime
import hashlib
import sys, json
import importlib
# import urllib.request

importlib.reload(sys)
# sys.setdefaultencoding('utf-8')
requests.packages.urllib3.disable_warnings()

# domain_name = 'http://172.20.50.13:8007/'
domain_name = 'http://api.ceshi.qichejianli.com/'
# domain_name = 'https://api.qichejianli.com/'

url = domain_name + 'resume/queryData/queryCarInfo'
# url = domain_name + 'queryData/queryCarInfo'
url_vin_check = domain_name + 'resume/queryData/vin/check'
url_vin_chake_report = domain_name + 'resume/info/getCarWBInfoByVin'
url_getWbCarInfo = domain_name + 'resume/queryData/getWbCarInfo'
# url_getWbCarInfo = domain_name + 'queryData/getWbCarInfo'
url_getWbCarInfoWG = domain_name + 'resume/queryData/getWbCarInfoWG'
url_valuation = domain_name + 'resume/queryData/valuation'
url_getCarList = domain_name + 'resume/info/getCarList'
url_queryPreCheckInfo = domain_name + 'resume/queryData/queryPreCheckInfo'
# url_queryPreCheckInfo = domain_name + 'queryData/queryPreCheckInfo'
headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
query_time = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')


def md5_encode(key):
    m = hashlib.md5()
    m.update(key.encode("utf-8"))
    return m.hexdigest()


def create_key(token, qudaoType, date):
    key = md5_encode(date + qudaoType + token)
    return key


# 测试u2test
# token = '14ffd96dccc95ffd547d1d9127ee851d'
# qudaoType = 'u2test'
# uxinpai测试
# token = '726ae9c03faf4ced36c5d0c1e24129c6'
# qudaoType = 'uxinpai'
# uxinpai
# token = '203047e8b6c811f2898b980030f4489e'
# qudaoType = 'uxinpai'
# U2自动审核测试
# token = '76b21302b846afa9d1cc31f00fb9bcd0'
# qudaoType = 'u2auto'
# U2自动审核线上
# token = '493d8529b6e661e1e11e746a79fd7ecb'
# qudaoType = 'u2auto'
# 潘多拉线上
# token = '689b5f44773a7f81b236a37a371c6045'
# qudaoType = 'zybatch'
# U2正式
token = '9dd4cc8d437a519af0ee5f184ab2ead4'
qudaoType = 'U2'
# 查克
# token = '8f9795a46f1ff0d0af620009004a7514'
# qudaoType = 'chake'
#  LDC661T35G3S861G6 查无记录
key = create_key(token, qudaoType, query_time)
vin = 'LDC643T30E3027271'
# LFV2A115093079664  LFV2A21J383039578  LDCC13T39D1560645 LDC703L29A1378029 textData LDC643T30E3027271
# LS5A3ADE3AB011620  LDCC23143E1047773  LFPM5ACP891E01601
data = {
    'qudaoType': qudaoType,
    'key': key,
    'date': query_time,
    'vinNo': vin,
    'engineNo': '11',
    'callBackUrl': 'http://192.168.85.232:8000/api/index?page_size=10&page=1',
    'qudaoDataType': 'textData',
    'makeId': '',
    'brandId': '',
    'makeName': '',
    'remark': ''
}

data_vin_check = {
    'qudaoType': qudaoType,
    'key': key,
    'date': query_time,
    'vinNo': vin
}

data_vin_chake_report = {
    'qudaoType': qudaoType,
    'key': key,
    'date': query_time,
    'vinNo': vin,
    'source': '2'
}
data_getWbCarInfo = {
    'qudaoType': qudaoType,
    'qudaoOrderId': '5127042',
}
data_getWbCarInfoWG = {
    'qudaoOrderId': '2000170'
}
data_valuation = {
    "qudaoType": qudaoType,
    "key": key,
    "date": query_time,
    "cityId": "201",
    "modeId": "114774",
    "mileage": "6.0",
    "registDate": "2013-07-01",
    "seriesId": "621",
    "condition": "B",
    "orderId": "794008",
    "estimate": "b2c"
}
data_queryPreCheckInfo = {
    'qudaoType': qudaoType,
    'key': key,
    'date': query_time,
    'qudaoOrderID': '3758691',
}
# 2005964
# 2000766  2000755
# queryCarInfo
res = requests.post(url, data=data, headers=headers, verify=False)
res_time = float(res.elapsed.microseconds) / 1000
print(res.text)
print(vin + u'下单响应时间:' + str(res_time) + u'ms')

# data1 = {
#     'qudaoType': 'uxinpai',
#     'key': 'c19d215ff8f122bac71d587a4dd7add0',
#     'date': '20180419 14:47:08',
#     'vinNo': vin,
#     'engineNo': '',
#     'callBackUrl': 'http://192.168.85.232:8000/api/index?page_size=10&page=1',
#     'qudaoDataType': 'textData',
#     'makeId': '',
#     'brandId': '',
#     'makeName': '',
#     'remark': ''
# }
# res1 = requests.post(url, data=data1, headers=headers, verify=False)
# print res1.text
# data2 = {
#     'qudaoType': 'chake',
#     'key': 'ef29e0b280ccdc21f7c5177a05ebe698',
#     'date': '20180419 14:59:31',
#     'vinNo': vin,
#     'engineNo': '',
#     'callBackUrl': 'http://192.168.85.232:8000/api/index?page_size=10&page=1',
#     'qudaoDataType': 'textData',
#     'makeId': '',
#     'brandId': '',
#     'makeName': '',
#     'remark': ''
# }
# res2 = requests.post(url, data=data2, headers=headers, verify=False)
# print res2.text

# resume/queryData/vin/check
# res1 = requests.post(url_vin_check, data=data_vin_check, headers=headers, verify=False)
# print res1.text

# resume/info/getCarWBInfoByVin  返回url
# res2 = requests.post(url_vin_chake_report, data=data_vin_chake_report, headers=headers, verify=False)
# print res2.text

# resume/queryData/getWbCarInfo
# res3 = requests.post(url_getWbCarInfo, data=data_getWbCarInfo, headers=headers, verify=False)
# print res3.text

# resume/queryData/valuation
# res4 = requests.post(url_valuation, data=data_valuation, headers=headers, verify=False)
# print res4.text


# resume/queryData/getCarList
# res5 = requests.post(url_getCarList, headers=headers, verify=False)
# print res5.text

# getWbCarInfoNew
# res6 = requests.post(url_getWbCarInfoWG, data=data_getWbCarInfoWG, headers=headers, verify=False)
# print res6.text

# url_queryPreCheckInfo
# res7 = requests.post(url_queryPreCheckInfo, data=data_queryPreCheckInfo, headers=headers)
# print res7.text


# for x in range(1, 20):
#     for y in range(1, 33):
#         z = 100 - x - y
#         if (z % 3 == 0) and (5 * x + 3 * y + z / 3 == 100):
#             print('公鸡：%s 母鸡：%s 小鸡：%s' % (x, y, z))

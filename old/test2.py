# -*- coding:utf-8 -*-
import requests
import json
import re
import pymysql
import contextlib
import random
import string

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'xin',
    'password': '48sdf37EB7',
    'db': 'routdata',
    'charset': 'utf8mb4',
    # 'cursorclass': pymysql.cursors.DictCursor,
}
url = 'http://juzhen.test.youxinpai.com/'
url_login = 'http://juzhen.test.youxinpai.com/cp/login/check/'
url_add = 'http://juzhen.test.youxinpai.com/cp/zb_manage/add_zb'
url_add_car = 'http://juzhen.test.youxinpai.com/cp/zb_manage/add_zb_car_act'
url_place_order = 'http://juzhen.test.youxinpai.com/cp/zb_manage/place_zb_order'
headers_login = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
data_login = 'username=zhouxin&password=C97JaTmZV%2FBUkqJdnmWXHZP75jqey7eDF1f8%2FuYHMLaJVSrK%2F6R4ObieZ2v68lDV75%2FdxFr%2FO31nv%2BxJ4%2FP4isGPnokR9zt4QEBZhxE0aEoXO%2FtKUKKEkOfzQR5%2FdgpYZd9b28v1dd4DVt9zJNUT3zoFzknndl5%2B021aDgX8yz8%3D'
data_add = 'batch_cost=530&batch_num=2&cost_days=7&from_city=201&from_province=2&get_car_address=%E8%AF%A6%E7%BB%86%E5%9C%B0%E5%9D%80&get_car_name=%E6%8E%A5%E8%BD%A6%E4%BA%BA%E5%A7%93%E5%90%8D&get_car_phone=18910034567&single_cost=680&to_city=1702&to_province=17&weituo_name=%E5%A7%94%E6%89%98%E4%BA%BA%E5%A7%93%E5%90%8D&weituo_phone=18910034563'
cookies = dict(PHPSESSID='3nre5ohv8ttugcessgo4krnti6')


# 3nre5ohv8ttugcessgo4krnti6

# resp = requests.get(url, verify=False, allow_redirects=False)
# g_cookie = resp.headers['set-cookie']
# print g_cookie
# p = re.compile(r'PHPSESSID=(.*?);')
# print p.findall(g_cookie)

# res = requests.post(url_login, data=data_login, headers=headers_login)
# print dir(res)
# print res.headers
# cookies = res.cookies
# print cookies
# print('; '.join(['='.join(item) for item in cookies.items()]))

@contextlib.contextmanager
def connect_mysql():
    conn = pymysql.connect(**config)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def add_zb(data_add):
    res1 = requests.post(url_add, data=data_add, headers=headers_login, cookies=cookies)
    p1 = re.compile(r'.*?("status":1).*?')
    # print p1.findall(res1.text)
    if p1.findall(res1.text):
        a = json.loads(res1.text)
        id = a['id']
        return id
    else:
        return 0


def check_order_id_zb(id):
    with connect_mysql() as cursor:
        sql = "select order_id_zb from order_zb where id = " + str(id) + ";"
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            order_id_zb = result['order_id_zb']
    return order_id_zb

    # conn = pymysql.connect(**config)
    # try:
    #     with conn.cursor() as cursor:
    #         sql = "select order_id_zb from order_zb where id = " + str(id) + ";"
    #         cursor.execute(sql)
    #         results = cursor.fetchall()
    #         for result in results:
    #             order_id_zb = result[0]
    # finally:
    #     conn.close()
    # return order_id_zb


def add_car(order_id_zb, car_no):
    data_add_car = {
        'order_id_zb': order_id_zb,
        'file_id': 'file_shc_',
        'source_type': '3',
        'service_type': '2',
        'brand_id': '2000000062',
        'series_id': '2000002036',
        'car_no': car_no,
        'vin': '1',
        'left_img': '/che/201710/1709/59e55d9557896346199.jpg',
        'file_shc_1': '1.jpg'
    }
    res2 = requests.post(url_add_car, data=data_add_car, headers=headers_login, cookies=cookies)
    # return res2.text
    p2 = re.compile(r'.*?("status":0).*?')
    if p2.findall(res2.text):
        return car_no
    else:
        return 1


def check_order_id(order_id_zb):
    with connect_mysql() as cursor:
        sql = "SELECT order_id FROM `car_for_trans` where order_id_zb =" + order_id_zb
        cursor.execute(sql)
        results = cursor.fetchall()
        list_order_id = []
        for result in results:
            list_order_id.append(result['order_id'])
    order_id_str = ''
    for i in list_order_id:
        order_id_str = order_id_str + str(i) + ','
    return order_id_str

    # conn = pymysql.connect(**config)
    # try:
    #     with conn.cursor() as cursor:
    #         sql = "SELECT order_id FROM `car_for_trans` where order_id_zb =" + order_id_zb
    #         cursor.execute(sql)
    #         results = cursor.fetchall()
    #         list_order_id = []
    #         for result in results:
    #             list_order_id.append(result[0])
    # finally:
    #     conn.close()
    # order_id_str = ''
    # for i in list_order_id:
    #     order_id_str = order_id_str + str(i) + ','
    # return order_id_str


def place_order(order_id_zb, order_id_str):
    data_place_order = {
        'order_id_zb': order_id_zb,
        'order_id_str': order_id_str
    }

    res3 = requests.post(url_place_order, data=data_place_order, headers=headers_login, cookies=cookies)
    # print res3.text


def get_car_no():
    pro = [u'京', u'津', u'黑', u'吉', u'辽', u'冀', u'豫', u'鲁', u'晋', u'陕', u'蒙', u'宁', u'甘', u'新', u'青', u'藏', u'鄂', u'皖',
           u'苏', u'沪', u'浙', u'闵', u'湘', u'赣', u'川', u'渝', u'贵', u'云', u'粤', u'桂', u'琼']
    city = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']
    no = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
          'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    car_no_bak = ''
    for i in random.choice(pro):
        for j in random.choice(city):
            for k in range(0, 5):
                for l in random.choice(no):
                    car_no_bak += l
            # no = string.join(random.sample(no, 5)).replace(" ", "")
            # car_no = i + j + no
            car_no = i + j + car_no_bak
    return car_no

def update_card_id(id):
    with connect_mysql() as cursor:
        sql = "select * from data_remark "
        cursor.execute(sql)
        results = cursor.fetchall()
        print(cursor.rowcount)

        for result in results:
            # print result['remark']
            print(result)


if __name__ == "__main__":
    update_card_id(1)

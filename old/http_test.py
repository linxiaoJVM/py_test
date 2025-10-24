# -*- coding: utf-8 -*-

import xlrd
import requests
import time

def post_vin(item):
    url = 'http://api.qichejianli.com/resume/api/defriendCarByVin'
    r = requests.post(url, data={'vinNo':item, 'token':'9dd4cc8d437a519af0ee5f184ab2ead4'})
    print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),r.text,r.headers

def get_test():
    url = 'http://10.70.93.79:8115/user/errortest'
    for i in range(50):
        r = requests.get(url)
        # time.sleep(0.1)
        print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),r.text,r.headers

if __name__ == '__main__':
    get_test()
    # defriend_car_by_vin('LBVPS510XBSD49615')
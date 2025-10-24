# -*- coding: utf-8 -*-

import xlrd
import requests
import time


def read_excel():
    data = xlrd.open_workbook(r'D:\resume_qudao_order.xlsx')
    print("UP %s"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    print(data.sheet_names())
    table = data.sheets()[0]          #通过索引顺序获取sheet

    nrows = table.nrows  #获取该sheet中的有效行数
    ncols = table.ncols   #获取列表的有效列数
    print (nrows, ncols)

    cols = table.col_values(0)  #第一列内容
    # print cols
    for item in cols:
        print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),item.strip()
        defriend_car_by_vin(item.strip())
        time.sleep(0.5)


def defriend_car_by_vin(item):
    url = 'http://api.qichejianli.com/resume/api/defriendCarByVin'
    r = requests.post(url, data={'vinNo':item, 'token':'9dd4cc8d437a519af0ee5f184ab2ead4'})
    print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),r.text,r.headers

if __name__ == '__main__':
    read_excel()
    # defriend_car_by_vin('LBVPS510XBSD49615')

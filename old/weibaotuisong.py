# -*- coding: utf-8 -*-

import xlrd
import requests
import time
# 读取txt文件
def read_txt():
    f = open(r"D:\asd.txt")               # 返回一个文件对象
    line = f.readline()
    while line:
        print line,
        line = f.readline()
    f.close()

# 读取csv文件
def read_csv():
    with open(r"D:\2018-09-11_124429_494.csv") as f:
        for line in f:
            print line,

# 读取excel文件
def read_excel():
    data = xlrd.open_workbook(r'D:\qwe.xlsx')
    print("UP %s"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    print data.sheet_names()
    table = data.sheets()[0]          #通过索引顺序获取sheet

    nrows = table.nrows  #获取该sheet中的有效行数
    ncols = table.ncols   #获取列表的有效列数
    print nrows,ncols

    cols = table.col_values(0)  #第一列内容
    # print cols
    for item in cols:
        print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),int(item)
        invoke_url(int(item))
        time.sleep(0.5)


def invoke_url(item):
    url = 'http://api.qichejianli.com/resume/queryData/rePushOrderNoticeStatus'
    r = requests.post(url, data={'qudaoOrderIDs':item})
    print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),r.text,r.headers

if __name__ == '__main__':
    read_csv()
    # defriend_car_by_vin('LBVPS510XBSD49615')

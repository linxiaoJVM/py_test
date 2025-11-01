'''
Created on 2020年1月30日

@author: JM
'''
import pandas as pd
import tushare as ts
from sqlalchemy import create_engine 

engine_ts = create_engine('mysql+pymysql://boss3:frJfx^ormd8aybpAp2@rm-2ze8vch3mlfl995kr90110.mysql.rds.aliyuncs.com/pinpoint')

def read_data():
    sql = """select * from stock_daily where cal_trade_date > '2025-05-28' ORDER BY cal_trade_date ASC"""
    # sql = """select * from stock_daily where ts_code='603516.SH' and cal_trade_date >= '2025-04-30' and cal_trade_date <= '2025-07-16' ORDER BY cal_trade_date"""
    df = pd.read_sql_query(sql, engine_ts)
    return df


def write_data(df):
    res = df.to_sql('stock_daily', engine_ts, index=False, if_exists='append', chunksize=5000)
    print(res)
    print("------------")

def write_stock_basic(df):
    res = df.to_sql('stock_basic', engine_ts, index=False, if_exists='append', chunksize=5000)
    print(res)
    print("------------")

def get_data():
    pro = ts.pro_api()
    df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    return df

def read_stock_basic_data():
    sql = """select ts_code,symbol,name,area,industry from stock_basic"""
    # sql = """select * from stock_daily where ts_code='603516.SH' and cal_trade_date >= '2025-04-30' and cal_trade_date <= '2025-07-16' ORDER BY cal_trade_date"""
    df = pd.read_sql_query(sql, engine_ts)
    return df

if __name__ == '__main__':
    # df = read_data()
    df = read_stock_basic_data()
    # print(df)
    # write_stock_basic(df)
    
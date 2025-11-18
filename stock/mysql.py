'''
Created on 2020年1月30日

@author: JM
'''
from urllib import parse
import pandas as pd
import tushare as ts
from sqlalchemy import create_engine 

user = "aa"
password = parse.quote_plus("frJfx")
host = "127.0.0.1"
database = "aa"

engine_ts = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')

def read_data():
    sql = """select * from stock_daily where cal_trade_date > '2025-05-28' ORDER BY cal_trade_date ASC"""
    # sql = """select * from stock_daily where ts_code='603516.SH' and cal_trade_date >= '2025-04-30' and cal_trade_date <= '2025-07-16' ORDER BY cal_trade_date"""
    df = pd.read_sql_query(sql, engine_ts)
    return df

def read_data_v2(end_date: str = ''):
    sql = f"""select * from stock_daily where cal_trade_date > '2025-05-20' and cal_trade_date <= '{end_date}' ORDER BY cal_trade_date ASC"""
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

def read_result_stock_data(start_time: str = '',end_date: str = ''):
    sql = f"""select ts_code,name,min(cal_trade_date) as cal_trade_date from result_stock where cal_trade_date >= '{start_time}' and cal_trade_date < '{end_date}' GROUP BY ts_code,name"""
    df = pd.read_sql_query(sql, engine_ts)
    return df

def read_data_v3(ts_code: str = '', start_time: str = '', end_date: str = ''):
    sql = f"""select * from stock_daily where ts_code='{ts_code}' and cal_trade_date >= '{start_time}' and cal_trade_date < '{end_date}' ORDER BY cal_trade_date ASC"""
    # sql = """select * from stock_daily where ts_code='603516.SH' and cal_trade_date >= '2025-04-30' and cal_trade_date <= '2025-07-16' ORDER BY cal_trade_date"""
    df = pd.read_sql_query(sql, engine_ts)
    return df

def write_result_stock(df):
    res = df.to_sql('result_stock', engine_ts, index=False, if_exists='append', chunksize=5000)
    print(res)
    print("------------")


def read_data_v4(ts_code: str = ''):
    sql = f"""select max(close) as max_close  from stock_daily where ts_code='{ts_code}'"""
    df = pd.read_sql_query(sql, engine_ts)
    return df

def read_data_v5(ts_code: str = '', end_date: str = ''):
    sql = f"""select * from stock_daily where ts_code='{ts_code}' and  cal_trade_date='{end_date}'"""
    df = pd.read_sql_query(sql, engine_ts)
    return df

if __name__ == '__main__':
    # df = read_data()
    df = read_result_stock_data()
    print(df)
    ts_code_list = df['ts_code'].to_list()
    print(ts_code_list)
    # write_stock_basic(df)
    
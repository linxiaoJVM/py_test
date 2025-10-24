'''
Created on 2020年1月30日

@author: JM
'''
import pandas as pd
import tushare as ts
from sqlalchemy import create_engine 

engine_ts = create_engine('mysql+pymysql://boss:boss@127.0.0.1/aa')

def read_data():
    sql = """SELECT * FROM stock_daily LIMIT 20"""
    df = pd.read_sql_query(sql, engine_ts)
    return df


def write_data(df):
    res = df.to_sql('stock_daily', engine_ts, index=False, if_exists='append', chunksize=5000)
    print(res)
    print("------------")


def get_data():
    pro = ts.pro_api()
    df = pro.stock_basic()
    return df


if __name__ == '__main__':
    df = read_data()
    # df = get_data()
    # write_data(df)
    print(df)
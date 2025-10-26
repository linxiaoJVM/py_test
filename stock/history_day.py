
# 导入tushare
from datetime import datetime
import time as time
import tushare as ts
import mysql as mysql
import pandas as pd

# 初始化pro接口
pro = ts.pro_api('9d347f0a583f4a2fb87dc561517723e00884ae6dd9f8b2b4ddb440da')

# c获取交易日
def get_trade_cal(start_date='', end_date=''):
    while True:
        df = pro.trade_cal(is_open='1', start_date=start_date, 
                            end_date=end_date)
        if df is None or len(df) == 0:
            print("未获取到数据，等待2秒后重试...")
            time.sleep(2)
        else:
            break
    return df
    # print(df)

# 按交易日获取当天所有的股票数据
def get_daily(trade_date=''):
    for i in range(5):
        try:
            while True:
                df = pro.daily(trade_date=trade_date)
                if df is None or len(df) == 0:
                    print("未获取到数据，等待2秒后重试...")
                    time.sleep(2)
                else:
                    break
        except:
            print("网络错误，等待(1+i)秒后重试...")
            time.sleep(1+i)
        else:
            return df
      
if __name__ == '__main__':
    # 获取交易日
    # start_date = '20000101'
    # end_date = '20041231'
    # trade_cal = get_trade_cal(start_date=start_date, end_date=end_date)

    # 每天数据，手动执行
    data = {
        "cal_date": ['20251024']
    }
    trade_cal = pd.DataFrame(data)

    # A股日线行情
    for date in trade_cal['cal_date'].values:
        print(date)
        df = get_daily(date)
        # print(df.head)
        df['pre_close'] = df['pre_close'].fillna(0)
        df['change'] = df['change'].fillna(0)
        df['pct_chg'] = df['pct_chg'].fillna(0)
        df['cal_trade_date'] = df['trade_date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
        mysql.write_data(df)
        # time.sleep(1)
        # break
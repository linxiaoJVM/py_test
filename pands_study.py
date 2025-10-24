import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import dask.dataframe as dd
import numba
import yfinance as yf
import os
from datetime import datetime
import stock.mysql as mysql

# s = pd.Series(np.array([1, 2, 3, 4]),index=['a', 'b', 'c', 'd'])
# print(s)
# print(s.iloc[1])

# 创建一个简单的 DataFrame
data = {
    # "AAPL": [150, 152, 153, 151, 155],
    # "GOOGL": [2800, 2820, 2810, 2830, 2840],
    # "AMZN": [3400, 3420, 3410, 3430, 3440],
    "cal_date": [20200101, 20200102, 20200103, 20200104, 20200123]
}
# data = [['Google', 10], ['Runoob', 12], ['Wiki', 13]]
# df = pd.DataFrame(data)
# # 查看 DataFrame
# print(df.info())
# print(df)
# df['trad_date'] = df['cal_date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
# print(df)
# print(df.loc[df['AAPL'] > 152,'AMZN'])
# print(df.iloc[1,0])
# print(df.loc[[0]])


# df = pd.read_csv('D:\\down\\nba.csv', sep='\t')
# print(df.info())
# print(df.head(10))


# 示例数据
# data = {
#     'Height': [150, 160, 170, 180, 190],
#     'Weight': [45, 55, 65, 75, 85],
#     'Age': [20, 25, 30, 35, 40]
# }
#
# df = pd.DataFrame(data)
#
# # 计算斯皮尔曼等级相关系数
# spearman_correlation = df.corr(method='spearman')
# print(spearman_correlation)

# 示例数据
# data = {
#     'Height': [150, 160, 170, 180, 190],
#     'Weight': [45, 55, 65, 75, 85],
#     'Age': [20, 25, 30, 35, 40]
# }
# df = pd.DataFrame(data)
# # 绘制相关性热图
# plt.figure(figsize=(8, 6))
# sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt='.2f', vmin=-1, vmax=1)
# plt.title('Correlation Heatmap')
# plt.show()

# 示例数据
# data = {'Name': ['Alice', 'Bob', 'Charlie', 'David'],
#         'Age': [25, 30, 35, 40],
#         'Salary': [50000, 60000, 70000, 80000]}

# df = pd.DataFrame(data)
# sortvalues = df.sort_values(by='Age', ascending=True)
# print(sortvalues)



# df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [5, 6, 7, 8]})
# df.set_index('A', inplace=True)
# print(df)

# date = datetime.strptime('20200123', '%Y%m%d')
# print(date)

# 示例函数
# @numba.jit
# def calculate_square(x):
#     return x ** 2

# # 使用 numba 加速计算
# df = pd.DataFrame({'A': [1, 2, 3, 4]})
# df['B'] = df['A'].apply(calculate_square)
# print(df)

# proxy = 'http://127.0.0.1:10808' # 代理设置，此处修改
# os.environ['HTTP_PROXY'] = proxy
# os.environ['HTTPS_PROXY'] = proxy

# 获取茅台（600519.SS）的股票数据，日期范围从 2020-01-01 到 2021-01-01
# stock_data = yf.download('300875.SZ', start='2024-01-01', end='2024-3-15')

# 计算 5 日和 10 日的移动平均线
# stock_data['SMA_5'] = stock_data['Close'].rolling(window=5).mean()
# stock_data['SMA_10'] = stock_data['Close'].rolling(window=10).mean()

#查看数据的前几行
# print(stock_data.head(10))

#绘制收盘价和移动平均线
# plt.figure(figsize=(12, 6))
# plt.plot(stock_data['Close'], label='Close Price')
# plt.plot(stock_data['SMA_5'], label='5-Day SMA')
# plt.plot(stock_data['SMA_10'], label='10-Day SMA')
# plt.title('Maotai Stock Price with Moving Averages', fontsize=14)
# plt.xlabel('Date', fontsize=12)
# plt.ylabel('Price (CNY)', fontsize=12)
# plt.legend()
# plt.grid(True)
# plt.show()

df = mysql.read_data()
print(df['close'].pct_change())
print(df['pct_chg'].rolling(window=5).std())

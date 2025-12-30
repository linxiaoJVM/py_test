import pandas as pd
import numpy as np
import talib
from datetime import datetime, timedelta
import os
from typing import Dict, List, Tuple
from MainForce import MainForce
import mysql as mysql
import history_day as history_day


'''
横盘股票筛选器
用于筛选出在指定时间段内横盘的股票
'''

class ConsolidationStock:
    def __init__(self):
        pass
        # self.detector = ConsolidationDetector()
    
    def load_all_stock_data(self, end_date='') -> Dict[str, pd.DataFrame]:
        """
        加载所有股票数据
        
        """
        # 处理后的股票数据
        stock_data = {}
        # 从MySQL加载数据
        if end_date == '':
            df = mysql.read_data()
        else:
            df = mysql.read_data_v2(end_date)
        # 按照股票代码分组
        grouped = df.groupby('ts_code')
        for ts_code, df_code in grouped:
            # 按照交易日期排序
            df_stock = df_code.sort_values('cal_trade_date', ascending=True)
            # 设置交易日期为索引
            df_stock.set_index('cal_trade_date', inplace=True)
            stock_data[ts_code] = df_stock
        
        print(f"成功加载 {len(stock_data)} 只股票数据")
        return stock_data
    
    def find_stocks(self,threshold=50, end_date='') -> pd.DataFrame:
        # 找出横盘的股票
        results = self.find_consolidation_stocks(threshold,end_date)
        # print(len(results))
        # 跟以前找出的股票对比，去重
        # remove_duplication_df = self.cal_duplication(pd.DataFrame(results))
        # print(remove_duplication_df)
        # 合并数据
        results_df = self.merge_stocks(pd.DataFrame(results))
        # 结果保存到数据库中
        self.save_result_to_db(results_df)
        return results_df

    def find_consolidation_stocks(self,threshold=50, end_date='') -> List[Dict]:
         
        """
          找出横盘指定天数的股票
        """
        print(f"开始加载股票数据...寻找横盘 {threshold} 天的股票")
        all_stocks = self.load_all_stock_data(end_date)
        
        results = []
        latest_date = ''
        
        for stock_code, data in all_stocks.items():
            if len(data) < threshold:
                continue

            # if stock_code != '000016.SZ':
            #     continue

            # print(f"分析股票: {stock_code}")
            # 只取最近threshold天的数据
            data = data.tail(n=threshold)

            # print(data.head())
            # 1、计算涨幅
            # 昨天收盘价
            pre_close = data.iloc[0]['pre_close']
            # 最后一天收盘价
            close = data['close'].iloc[-1]

            # 股价小于 10块的 不考虑
            if close < 10:
                continue

            # print(f"pre_close: {pre_close}, close: {close}")
            # 获取最新一天的日期 trade_date
            # latest_date = data.index[-1]
            if latest_date == '':
                latest_date = data.index[-1].strftime('%Y%m%d')

            # 计算涨幅
            if pre_close != 0:
               price_range_pct = (close - pre_close) / pre_close
            else:
                price_range_pct = 0
            
            # print(f"股票: {stock_code}, 涨幅: {price_range_pct:.2%}")

            #2、计算振幅
            high = data['high']
            low = data['low']
            # print(f"high max: {high.max()}, low min: {low.min()}")

            if low.min() != 0:
               amplitude = (high.max() - low.min()) / low.min()
            else:
               amplitude = 0
            # print(f"股票: {stock_code}, 振幅: {amplitude:.2%}")

            #3、计算波动率
            pct_chg = data['pct_chg']
            volatility = pct_chg.std()
            # print(f"股票: {stock_code}, 波动率: {volatility:.2f}%")

            # 4、是否突破箱体，不包括最后一天(最后一天的收盘价，是否大于前面收盘价的最高价)
            # print(high[:-1].max())
            break_out = False
            if close > data['close'][:-1].max():
                # print(f"股票: {stock_code}, 突破箱体")
                break_out = True
            else:
                # print(f"股票: {stock_code}, 未突破箱体")
                break_out = False

            # 5、连续三天上涨
            three_day_rise = False
            if (pct_chg.iloc[-3:] > 0).all():
                # print(f"股票: {stock_code}, 连续三天上涨")
                three_day_rise = True
            else:
                # print(f"股票: {stock_code}, 未连续三天上涨")
                three_day_rise = False
            
            # 最后一天的成交量是否大于前一天成交量的1.6倍
            volume_increase = False
            if data['vol'].iloc[-1] >= 1.6 * data['vol'].iloc[-2]:
                volume_increase = True
        
            
            # 综合评分
            score = 0
            if 0 < price_range_pct <= 0.15:  # 总涨幅小于15%
                score += 1
            if amplitude <= 0.20:  # 总振幅小于20%
                score += 1
            if volatility < 3.0:    # 波动率小于3%
                score += 1
            # 判断是否为横盘 (至少满足3个条件)
            is_consolidation = score >= 3
            # 突破箱体必须要放量
            if is_consolidation and break_out and volume_increase:
                results.append({
                    'stock_code': stock_code,
                    'volatility': volatility,
                    'price_range_pct': price_range_pct,
                    'amplitude': amplitude,
                    'break_out': break_out,
                    'three_day_rise': three_day_rise,
                    'trade_date': latest_date,
                    'current_close': close,
                    'consolidation_score': score
                })
        return results
       

    def cal_duplication(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算重复数据
        """
        # 从数据库中找出已经算出的股票
        result_df = mysql.read_result_stock_data()
        ts_code_list = result_df['ts_code'].to_list()

        duplication = df[df['stock_code'].isin(ts_code_list)]
        print(f"找到 {len(duplication)} 只重复的股票，已剔除")
        print(duplication)
        # 把df中stock_code在ts_code_list中的数据删除
        df = df[~df['stock_code'].isin(ts_code_list)]
        return df

    def merge_stocks(self, results: pd.DataFrame) -> pd.DataFrame:
        basic = []
        for _, r in results.iterrows():
            # print(r['stock_code'], r['price_range_pct'], r['amplitude'], r['volatility'])
            # 获取股票每日指标信息
            df = history_day.daily_basic(r['stock_code'], r['trade_date'])
            df['pe'] = df['pe'].fillna(0)
            df['pe_ttm'] = df['pe_ttm'].fillna(0)

            # 找出当前股票历史中的最高价
            max_close_df = mysql.read_data_v4(ts_code=r['stock_code'])
            max_close = max_close_df['max_close'].values[0]
            # 计算当前价格在历史最高价中的比例
            price_position = r['current_close'] / float(max_close)


            basic.append({
                'ts_code': df['ts_code'].values[0],
                'turnover_rate': df['turnover_rate'].values[0],
                'volume_ratio': df['volume_ratio'].values[0],
                'pe': df['pe'].values[0],
                'pe_ttm': df['pe_ttm'].values[0],
                'pb': df['pb'].values[0],
                'total_mv': df['total_mv'].values[0],
                'circ_mv': df['circ_mv'].values[0],
                'max_close': max_close,
                'price_position': price_position
            })

        # print(pd.DataFrame(basic))
        # 合并每日指标数据
        result = pd.merge(results, pd.DataFrame(basic), left_on='stock_code', right_on='ts_code', how='left')

        # 关联股票基本信息
        stock_basic = mysql.read_stock_basic_data()
        # 合并股票基本信息
        result = pd.merge(result, stock_basic, left_on='stock_code', right_on='ts_code', how='left')
        # if not result_df.empty:
        #     result_df = result_df.sort_values('consolidation_days', ascending=False)

        result = result.drop(columns=['ts_code_x', 'ts_code_y'])
        # 过滤掉市盈率为0的股票
        # result = result[result['pe'] > 0]
        # 过滤掉流通市值小于50亿的股票
        result = result[result['circ_mv'] > 500000.0]

        # 将市值转化成亿为单位
        result['total_mv'] = result['total_mv'] / 10000.0
        result['circ_mv'] = result['circ_mv'] / 10000.0

        # 总市值四舍五入保留两位小数
        result['total_mv'] = result['total_mv'].round(2)
        result['circ_mv'] = result['circ_mv'].round(2)

        result['price_range_pct'] = result['price_range_pct'].round(2)
        result['volatility'] = result['volatility'].round(2)
        result['amplitude'] = result['amplitude'].round(2)
        result['price_position'] = result['price_position'].round(2)

        # 转换数据类型
        result['price_range_pct'] = result['price_range_pct'].astype(float)
        result['volatility'] = result['volatility'].astype(float)
        result['amplitude'] = result['amplitude'].astype(float)
        result['price_position'] = result['price_position'].astype(float)

        # 把 price_position 换算成百分比显示
        # result['price_position'] = result['price_position'].apply(lambda x: f"{x:.2%}")
        new_order = ['stock_code', 'name', 'area', 'industry','trade_date', 'volatility', 'price_range_pct', 'amplitude', 'break_out',
                     'three_day_rise', 'current_close', 'max_close', 'price_position','turnover_rate', 'volume_ratio', 'pe', 'pe_ttm', 'pb', 'total_mv', 'circ_mv', 'consolidation_score']
        result = result[new_order]
        # 将列标题转换为中文
        result = result.rename(columns={
            'stock_code': '股票代码',
            'volatility': '波动率',
            'price_range_pct': '涨幅',
            'amplitude': '振幅',
            'break_out': '是否突破箱体',
            'three_day_rise': '是否连续三天上涨',
            'current_close': '当前价格(选中日)',
            'max_close': '历史最高价',
            'price_position': '当前价格在历史最高价中的占比',
            'trade_date': '选中日期',
            'consolidation_score': '整理评分',
            'turnover_rate': '换手率',
            'volume_ratio': '量比',
            'pe': '市盈率',
            'pe_ttm': '市盈率(TTM)',
            'pb': '市净率',
            'total_mv': '总市值(亿)',
            'circ_mv': '流通市值(亿)',
            'name': '股票名称',
            'area': '地区',
            'industry': '行业'
        })
        return result
    
    def save_result_to_db(self, df: pd.DataFrame):
        # 只需要 股票代码，股票名称，trade_date 字段

        df = df[['股票代码', '股票名称', '选中日期']]
        df = df.rename(columns={
             '股票代码': 'ts_code',
             '股票名称': 'name',
             '选中日期': 'cal_trade_date',
        })
        df['cal_trade_date'] = df['cal_trade_date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
        # print(df)
        mysql.write_result_stock(df)


    def benchmark_stocks(self, end_date='', result_start_date='', result_end_date='') -> pd.DataFrame:
         
        """
          计算选出股票的盈利指标
        """
        # 从数据库加载选出的股票数据
        result_df = mysql.read_result_stock_data(result_start_date,result_end_date)

        results = []
        for index, data in result_df.iterrows():
            stock_code = data['ts_code']
            print(f"分析股票: {stock_code}")

            # 从数据库加载当前股票的历史数据
            df = mysql.read_data_v3(ts_code=stock_code, start_time=data['cal_trade_date'], end_date=end_date)
            if df.empty:
                print(f"股票: {stock_code} 在 {data['cal_trade_date']} 到 {end_date} 之间无数据，跳过")
                continue
            if len(df) < 3:
                print(f"股票: {stock_code} 在 {data['cal_trade_date']} 到 {end_date} 之间数据不足，跳过")
                continue
            # # 第三天涨跌幅计算
            # third_day_pct_chg = df['pct_chg'].iloc[2] if len(df) > 2 else 0
            # # 第五天涨跌幅计算
            # fifth_day_pct_chg = df['pct_chg'].iloc[4] if len(df) > 4 else 0
            # # 第七天涨跌幅计算
            # seventh_day_pct_chg = df['pct_chg'].iloc[6] if len(df) > 6 else 0

            # 1、计算涨幅
            # 第一天收盘价
            pre_close = df.iloc[0]['close']
            # 最后一天收盘价
            close = df['close'].iloc[-1]

            # 计算涨幅
            if pre_close != 0:
               price_range_pct = (close - pre_close) / pre_close
            else:
                price_range_pct = 0
            
            # print(f"股票: {stock_code}, 涨幅: {price_range_pct:.2%}")

            #2、计算振幅
            high = df['high']
            low = df['low']
            # print(f"high max: {high.max()}, low min: {low.min()}")

            if low.min() != 0:
               amplitude = (high.max() - low.min()) / low.min()
            else:
               amplitude = 0
            # print(f"股票: {stock_code}, 振幅: {amplitude:.2%}")

            #3、计算波动率
            pct_chg = df['pct_chg'].astype(float)
            volatility = pct_chg.std()
            # print(f"股票: {stock_code}, 波动率: {volatility:.2f}%")

            # 4、计算最大回撤，应该找出最大值后面的最小值才是正确的最大回撤

            roll_max = (df['close'].max() - df['close'].min()) / df['close'].max()
            # 找出当前股票历史中的最高价
            max_close_df = mysql.read_data_v4(ts_code=stock_code)
            max_close = max_close_df['max_close'].values[0]

            # 查询当前股票，被计算出来的那天的行情数据
            stock_current_df = mysql.read_data_v5(ts_code=stock_code, end_date=data['cal_trade_date'])
            current_close = 0
            price_position = 0.0
            if not stock_current_df.empty:
                current_close = stock_current_df['close'].values[0]
                # 计算当前价格在历史最高价中的比例
                price_position = current_close / max_close

            # 用 end_date 计算出前一年的时间
            main_start_time = (datetime.strptime(end_date, '%Y-%m-%d') - pd.DateOffset(years=1)).strftime('%Y-%m-%d')
            main_df = mysql.read_data_v3(ts_code=stock_code, start_time=main_start_time, end_date=end_date)
            # 3. 检查控盘形态
            is_controlled, msg3 = MainForce.check_small_bull_trend(main_df)
            controll_value = '非控盘形态'
            if is_controlled:
                controll_value = '控盘形态'

            # 4. 检查底部放量
            bottom_vol_value = '非底部堆量'
            is_bottom_vol, msg4 = MainForce.check_bottom_volume(main_df)
            if is_bottom_vol:
                bottom_vol_value = '底部堆量'

            # print(f"股票: {stock_code}, 最大回撤: {max_drawdown:.2%}")
            # price_range_pct 精确两位小数
            price_range_pct = round(price_range_pct, 4)
            volatility = round(volatility, 4)
            amplitude = round(amplitude, 4)
            roll_max = round(roll_max, 4)
            price_position = round(price_position, 4)

            results.append({
                'stock_code': stock_code,
                'volatility': volatility,
                'price_range_pct': price_range_pct,
                'amplitude': amplitude,
                'roll_max': roll_max,
                'trade_date': data['cal_trade_date'],
                'max_close': max_close,
                'current_close': current_close,
                'price_position': price_position,
                'controll_status': controll_value,
                'bottom_vol_status': bottom_vol_value
            })
        
        results_df = pd.DataFrame(results)
        # 关联股票基本信息
        stock_basic = mysql.read_stock_basic_data()
        # 合并股票基本信息
        results_df = pd.merge(results_df, stock_basic, left_on='stock_code', right_on='ts_code', how='left')

        results_df = results_df.drop(columns=['ts_code'])
        # 转换数据类型
        results_df['price_range_pct'] = results_df['price_range_pct'].astype(float)
        results_df['volatility'] = results_df['volatility'].astype(float)
        results_df['amplitude'] = results_df['amplitude'].astype(float)
        results_df['roll_max'] = results_df['roll_max'].astype(float)
        # 把 price_position 换算成百分比显示
        results_df['price_position'] = results_df['price_position'].apply(lambda x: f"{x:.2%}")

        # 按照涨幅排序
        results_df = results_df.sort_values('price_range_pct', ascending=False)

        # 将列标题转换为中文
        results_df = results_df.rename(columns={
            'stock_code': '股票代码',
            'volatility': '波动率',
            'price_range_pct': '涨幅',
            'amplitude': '振幅',
            'roll_max': '最大回撤',
            'trade_date': '选中日期',
            'current_close': '当前价格(选中日)',
            'max_close': '历史最高价',
            'price_position': '当前价格在历史最高价中的占比',
            'controll_status': '控盘状态',
            'bottom_vol_status': '底部堆量'
        })
        return results_df
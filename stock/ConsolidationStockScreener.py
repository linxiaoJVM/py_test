import pandas as pd
import numpy as np
import talib
from datetime import datetime, timedelta
import os
from typing import Dict, List, Tuple
import mysql as mysql


'''
横盘股票筛选器
用于筛选出在指定时间段内横盘的股票
'''
class ConsolidationStockScreener:
    def __init__(self):
        pass
        # self.detector = ConsolidationDetector()
    
    def load_all_stock_data(self) -> Dict[str, pd.DataFrame]:
        """
        加载所有股票数据
        
        """
        # 处理后的股票数据
        stock_data = {}
        # 从MySQL加载数据
        df = mysql.read_data()
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
    
    def find_consolidation_stocks(self, 
                                min_days: int = 10, 
                                max_days: int = 60,
                                volatility_threshold: float = 0.015) -> pd.DataFrame:
        """
        找出横盘指定天数的股票
        """
        print("开始加载股票数据...")
        all_stocks = self.load_all_stock_data()
        
        results = []
        
        for stock_code, data in all_stocks.items():
            print(f"分析股票: {stock_code}")
            try:
                # 从今天往前检查
                consolidation_info = self._check_consolidation_period(
                    data, min_days, max_days, volatility_threshold
                )
                
                if consolidation_info['found']:
                    results.append({
                        'stock_code': stock_code,
                        'consolidation_days': consolidation_info['days'],
                        'start_date': consolidation_info['start_date'],
                        'end_date': consolidation_info['end_date'],
                        'volatility': consolidation_info['volatility'],
                        'price_range_pct': consolidation_info['price_range_pct'],
                        'atr_ratio': consolidation_info['atr_ratio'],
                        'volume_ratio': consolidation_info['volume_ratio'],
                        'consolidation_score': consolidation_info['score']
                    })
                    
            except Exception as e:
                print(f"分析股票 {stock_code} 时出错: {e}")
                continue
        
        # 创建结果DataFrame并按横盘天数排序
        result_df = pd.DataFrame(results)
        if not result_df.empty:
            result_df = result_df.sort_values('consolidation_days', ascending=False)
        
        return result_df
    
    def _check_consolidation_period(self, 
                                  data: pd.DataFrame, 
                                  min_days: int, 
                                  max_days: int,
                                  volatility_threshold: float) -> Dict:
        """
        检查单只股票的横盘周期
        """
        if len(data) < min_days:
            return {'found': False, 'reason': '数据不足'}
        
        # 从今天往前找
        end_date = data.index.max()
        start_check_date = end_date - timedelta(days=max_days)
        
        # 筛选检查期间的数据
        check_data = data[(data.index >= start_check_date) & (data.index <= end_date)]
        
        if len(check_data) < min_days:
            return {'found': False, 'reason': '检查期内数据不足'}
        
        # 滑动窗口检测横盘
        max_consolidation_days = 0
        best_start_date = None
        best_volatility = None
        best_range_pct = None
        best_volume_ratio = None
        best_score = 0
        
        # 从不同的起点开始检查
        for start_idx in range(len(check_data) - min_days + 1):
            for window_size in range(min_days, min(len(check_data) - start_idx, max_days) + 1):
                window_data = check_data.iloc[start_idx:start_idx + window_size]
                
                if len(window_data) < min_days:
                    continue
                
                # 检查这个窗口是否符合横盘条件
                is_consolidation, metrics = self._is_consolidation_window(
                    window_data, volatility_threshold
                )
                
                if is_consolidation and window_size > max_consolidation_days:
                    max_consolidation_days = window_size
                    best_start_date = window_data.index[0]
                    best_volatility = metrics['volatility']
                    best_range_pct = metrics['price_range_pct']
                    best_atr_ratio = metrics['atr_ratio']
                    best_volume_ratio = metrics['volume_ratio']
                    best_score = metrics['score']
        
        if max_consolidation_days >= min_days:
            return {
                'found': True,
                'days': max_consolidation_days,
                'start_date': best_start_date,
                'end_date': end_date,
                'volatility': best_volatility,
                'price_range_pct': best_range_pct,
                'atr_ratio': best_atr_ratio,
                'volume_ratio': best_volume_ratio,
                'score': best_score
            }
        else:
            return {'found': False, 'reason': '未找到符合条件的横盘周期'}
        
    def _is_consolidation_window(self, 
                               window_data: pd.DataFrame, 
                               volatility_threshold: float) -> Tuple[bool, Dict]:
        """
        判断指定时间窗口是否符合横盘条件
        """
        close = window_data['close']
        high = window_data['high']
        low = window_data['low']
        volume = window_data['vol']
        pct_chg = window_data['pct_chg']
        
        # 1. 价格波动率
        # returns = close.pct_change()
        volatility = pct_chg.std()
        
        # 2. 价格区间
        price_range_pct = (high.max() - low.min()) / close.mean()
        
        # 3. ATR相对波动
        atr = talib.ATR(high, low, close, timeperiod=14)
        atr_ratio = atr.mean() / close.mean()
        
        # 4. 成交量分析
        if len(volume) > 20:
            volume_short = volume.tail(10).mean()
            volume_long = volume.mean()
            volume_ratio = volume_short / volume_long if volume_long > 0 else 1
        else:
            volume_ratio = 1
        
        # 5. 布林带收缩
        bb_upper = talib.BBANDS(close, timeperiod=10, nbdevup=2, nbdevdn=2)[0]
        bb_lower = talib.BBANDS(close, timeperiod=10, nbdevup=2, nbdevdn=2)[2]
        bb_width = (bb_upper - bb_lower) / close
        avg_bb_width = bb_width.mean()
        
        # 综合评分
        score = 0
        if volatility < volatility_threshold:
            score += 1
        if price_range_pct < 0.1:  # 总波动小于10%
            score += 1
        if atr_ratio < 0.02:
            score += 1
        if avg_bb_width < 0.1:
            score += 1
        if volume_ratio < 1.2:  # 成交量没有明显放大
            score += 1
        
        # 判断是否为横盘 (至少满足3个条件)
        is_consolidation = score >= 3
        
        metrics = {
            'volatility': volatility,
            'price_range_pct': price_range_pct,
            'atr_ratio': atr_ratio,
            'volume_ratio': volume_ratio,
            'bb_width': avg_bb_width,
            'score': score
        }
        
        return is_consolidation, metrics
    
    # 横盘选择器 v2
    def find_consolidation_stocks_2(self,threshold=30) -> pd.DataFrame:
         
        """
          找出横盘指定天数的股票
        """
        print("开始加载股票数据...")
        all_stocks = self.load_all_stock_data()
        
        results = []
        
        for stock_code, data in all_stocks.items():
            if len(data) < threshold:
                continue

            # if stock_code != '000016.SZ':
            #     continue

            print(f"分析股票: {stock_code}")
            # 只取最近threshold天的数据
            data = data.tail(n=threshold)

            # print(data.head())
            # 1、计算涨幅
            # 昨天收盘价
            pre_close = data.iloc[0]['pre_close']
            # 最后一天收盘价
            close = data['close'].iloc[-1]
            # print(f"pre_close: {pre_close}, close: {close}")

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

            # 4、是否突破箱体，不包括最后一天
            # print(high[:-1].max())
            break_out = False
            if close > high[:-1].max():
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
            
            # 综合评分
            score = 0
            if 0 < price_range_pct < 0.25:  # 总涨幅小于25%
                score += 1
            if amplitude < 0.3:  # 总振幅小于30%
                score += 1
            if volatility < 3.0:    # 波动率小于3%
                score += 1
            # 判断是否为横盘 (至少满足3个条件)
            is_consolidation = score >= 3

            if is_consolidation and break_out:
                            results.append({
                                'stock_code': stock_code,
                                'volatility': volatility,
                                'price_range_pct': price_range_pct,
                                'amplitude': amplitude,
                                'break_out': break_out,
                                'three_day_rise': three_day_rise,
                                'consolidation_score': score
                            })
        
        result_df = pd.DataFrame(results)
        # 关联股票基本信息
        stock_basic = mysql.read_stock_basic_data()
        result = pd.merge(result_df, stock_basic, left_on='stock_code', right_on='ts_code', how='left')
        # if not result_df.empty:
        #     result_df = result_df.sort_values('consolidation_days', ascending=False)
        
        return result
    

    # 横盘选择器 v3
    def find_consolidation_stocks_3(self,threshold=50) -> pd.DataFrame:
         
        """
          找出横盘指定天数的股票
        """
        print(f"开始加载股票数据...寻找横盘 {threshold} 天的股票")
        all_stocks = self.load_all_stock_data()
        
        results = []
        
        for stock_code, data in all_stocks.items():
            if len(data) < threshold:
                continue

            # if stock_code != '000016.SZ':
            #     continue

            print(f"分析股票: {stock_code}")
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

            if is_consolidation and break_out:
                            results.append({
                                'stock_code': stock_code,
                                'volatility': volatility,
                                'price_range_pct': price_range_pct,
                                'amplitude': amplitude,
                                'break_out': break_out,
                                'three_day_rise': three_day_rise,
                                'consolidation_score': score
                            })
        
        result_df = pd.DataFrame(results)
        # 关联股票基本信息
        stock_basic = mysql.read_stock_basic_data()
        result = pd.merge(result_df, stock_basic, left_on='stock_code', right_on='ts_code', how='left')
        # if not result_df.empty:
        #     result_df = result_df.sort_values('consolidation_days', ascending=False)
        
        return result
import pandas as pd
import numpy as np
import talib
from datetime import datetime, timedelta
import os
from typing import Dict, List, Tuple

class ConsolidationDetector:
    def __init__(self):
        pass
    
    def detect_consolidation_advanced(self, data: pd.DataFrame, lookback_days: int = 360) -> Dict:
        """
        高级横盘检测，分析指定回溯期内的横盘情况
        """
        results = {}
        
        # 确保数据足够长
        if len(data) < lookback_days:
            lookback_days = len(data)
        
        analysis_data = data.tail(lookback_days)
        
        # 多种横盘检测方法
        methods = [
            self._volatility_consolidation,
            self._atr_consolidation, 
            self._bollinger_squeeze,
            self._price_channel_consolidation,
            self._moving_average_consolidation
        ]
        
        consolidation_scores = []
        consolidation_periods = []
        
        for method in methods:
            score, period = method(analysis_data)
            consolidation_scores.append(score)
            if period > 0:
                consolidation_periods.append(period)
        
        # 综合评分
        avg_score = np.mean(consolidation_scores)
        max_period = max(consolidation_periods) if consolidation_periods else 0
        
        results['consolidation_score'] = avg_score
        results['max_consolidation_period'] = max_period
        results['is_consolidating'] = avg_score > 0.6 and max_period >= 20
        
        # 详细指标
        detailed_metrics = self._get_detailed_metrics(analysis_data)
        results.update(detailed_metrics)
        
        return results
    
    def _volatility_consolidation(self, data: pd.DataFrame) -> Tuple[float, int]:
        """基于波动率的横盘检测"""
        close = data['close']
        
        # 计算滚动波动率
        volatility = close.pct_change().rolling(20).std()
        
        # 低波动天数
        low_vol_days = (volatility < 0.015).sum()
        low_vol_ratio = low_vol_days / len(volatility.dropna())
        
        return low_vol_ratio, low_vol_days
    
    def _atr_consolidation(self, data: pd.DataFrame) -> Tuple[float, int]:
        """基于ATR的横盘检测"""
        high, low, close = data['high'], data['low'], data['close']
        
        atr = talib.ATR(high, low, close, timeperiod=14)
        atr_ratio = atr / close
        
        # 低ATR天数
        low_atr_days = (atr_ratio < 0.02).sum()
        low_atr_ratio = low_atr_days / len(atr_ratio.dropna())
        
        return low_atr_ratio, low_atr_days
    
    def _bollinger_squeeze(self, data: pd.DataFrame) -> Tuple[float, int]:
        """布林带收缩检测"""
        close = data['close']
        
        bb_upper = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)[0]
        bb_lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)[2]
        bb_width = (bb_upper - bb_lower) / close
        
        # 历史布林带宽度比较
        bb_width_ma = bb_width.rolling(60).mean()
        squeeze_days = (bb_width < bb_width_ma * 0.7).sum()
        squeeze_ratio = squeeze_days / len(bb_width.dropna())
        
        return squeeze_ratio, squeeze_days
    
    def _price_channel_consolidation(self, data: pd.DataFrame) -> Tuple[float, int]:
        """价格通道横盘检测"""
        high, low, close = data['high'], data['low'], data['close']
        
        # 20日价格通道
        high_20 = high.rolling(20).max()
        low_20 = low.rolling(20).min()
        channel_width = (high_20 - low_20) / close
        
        narrow_channel_days = (channel_width < 0.08).sum()
        narrow_ratio = narrow_channel_days / len(channel_width.dropna())
        
        return narrow_ratio, narrow_channel_days
    
    def _moving_average_consolidation(self, data: pd.DataFrame) -> Tuple[float, int]:
        """均线收敛检测"""
        close = data['close']
        
        # 多条均线
        ma5 = close.rolling(5).mean()
        ma20 = close.rolling(20).mean()
        ma60 = close.rolling(60).mean()
        
        # 均线距离
        ma_distance = pd.DataFrame({
            'ma5_ma20': abs(ma5 - ma20) / close,
            'ma20_ma60': abs(ma20 - ma60) / close
        })
        
        max_distance = ma_distance.max(axis=1)
        convergence_days = (max_distance < 0.03).sum()
        convergence_ratio = convergence_days / len(max_distance.dropna())
        
        return convergence_ratio, convergence_days
    
    def _get_detailed_metrics(self, data: pd.DataFrame) -> Dict:
        """获取详细指标"""
        close = data['close']
        high = data['high']
        low = data['low']
        volume = data['volume']
        
        metrics = {}
        
        # 基础波动指标
        metrics['total_return_pct'] = (close.iloc[-1] / close.iloc[0] - 1) * 100
        metrics['max_drawdown'] = (close / close.expanding().max() - 1).min() * 100
        metrics['volatility_20d'] = close.pct_change().rolling(20).std().iloc[-1]
        
        # 价格区间
        metrics['price_range_20d'] = (high.tail(20).max() - low.tail(20).min()) / close.tail(20).mean()
        metrics['price_range_60d'] = (high.tail(60).max() - low.tail(60).min()) / close.tail(60).mean()
        
        # 成交量特征
        metrics['volume_ratio_20v60'] = volume.tail(20).mean() / volume.tail(60).mean()
        
        return metrics
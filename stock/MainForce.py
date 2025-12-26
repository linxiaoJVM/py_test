
import pandas as pd

'''
横盘股票筛选器
用于筛选股票中是否有主力的存在
'''
class MainForce:
    def __init__(self):
        pass


    """
    1. 转化“股东人数减少” (筹码集中)
    定性： 股东人数连续减少。
    定量： (本期股东人数 - 上期股东人数) / 上期股东人数 < -10% （降幅超过10%）。
    """
    def check_chip_concentration(df_holders):
        """
        df_holders: 包含股东人数的DataFrame，按日期排序
        列名假设: ['end_date', 'holder_num']
        """
        # 计算环比变化率
        df_holders['pct_change'] = df_holders['holder_num'].pct_change()
        
        # 获取最近一期的变化
        latest_change = df_holders['pct_change'].iloc[-1]
        
        # 连续两期减少 (可选)
        prev_change = df_holders['pct_change'].iloc[-2]
        
        # 判定标准：最近一期减少超过5%，或者连续两期都在减少
        if latest_change < -0.05 or (latest_change < 0 and prev_change < 0):
            return True, f"筹码集中: 最新一期减少 {latest_change:.2%}"
        
        return False, "筹码未明显集中"

    """
    2. 转化“逆势抗跌” (Alpha 属性)
    定性： 大盘跌，它不跌。
    定量： 在基准指数（如沪深300）跌幅 > 1% 的交易日里，该个股的涨跌幅 > -0.5% (甚至 > 0)。
    """
    def check_resilience(df_stock, df_benchmark, window=20):
        """
        df_stock: 个股日线数据
        df_benchmark: 大盘指数日线数据 (如上证指数)
        window: 回测最近多少天
        """
        # 合并数据，对齐日期
        df = pd.merge(df_stock[['date', 'pct_chg']], 
                    df_benchmark[['date', 'pct_chg']], 
                    on='date', suffixes=('_stock', '_index'))
        
        # 截取最近 window 天
        df_recent = df.tail(window)
        
        # 筛选大盘大跌的日子 (跌幅超过 1%)
        drop_days = df_recent[df_recent['pct_chg_index'] < -1.0]
        
        if len(drop_days) == 0:
            return False, "近期无大盘大跌日，无法测试抗跌性"
        
        # 计算个股在这些日子的表现
        # 抗跌标准：个股跌幅小于0.5% (即 > -0.5)，或者反而上涨
        resilient_days = drop_days[drop_days['pct_chg_stock'] > -0.5]
        
        resilience_score = len(resilient_days) / len(drop_days)
        
        # 如果抗跌率超过 80%
        if resilience_score >= 0.8:
            return True, f"强抗跌: 在大盘大跌的{len(drop_days)}天中，有{len(resilient_days)}天抗住"
        
        return False, "抗跌性一般"

    """
    3、转化“碎步小阳” (控盘程度)
    定性： K线整齐，小阳线多，沿着均线爬升。

    定量：
    趋势向上： 20日均线 > 60日均线。
    波动率低： 收盘价的标准差小（没有暴涨暴跌）。
    阳线占比高： 最近20天里，收盘价 > 开盘价的天数超过 60%。
    实体小： 平均K线实体幅度 < 2%。
    """
    def check_small_bull_trend(df_stock, window=20):
        """
        检查是否是主力控盘的碎步小阳
        """
        subset = df_stock.tail(window).copy()
        
        # 1. 均线多头排列 (假设df里已经算好了ma20, ma60)
        current_ma20 = subset['ma20'].iloc[-1]
        current_ma60 = subset['ma60'].iloc[-1]
        if current_ma20 <= current_ma60:
            return False, "非上升趋势"
            
        # 2. 阳线占比 (Close > Open)
        bull_days = len(subset[subset['close'] > subset['open']])
        bull_ratio = bull_days / window
        
        # 3. K线实体大小 (abs(Close - Open) / Open)
        # 主力控盘通常不会每天拉涨停，而是每天涨一点点
        subset['body_size'] = abs(subset['close'] - subset['open']) / subset['open']
        avg_body_size = subset['body_size'].mean()
        
        # 判定：阳线多(>60%) 且 实体小(<2.5%)
        if bull_ratio > 0.6 and avg_body_size < 0.025:
            return True, f"主力控盘: 阳线占比{bull_ratio:.0%}, 平均实体{avg_body_size:.2%}"
            
        return False, "形态不符合碎步小阳"

    """
    4. 转化“底部堆量” (资金进场)
    逻辑翻译：
    定性： 价格在低位，成交量比以前放大。
    定量：
    位置低： 当前价格处于过去250天（一年）的 30% 分位以下。
    量能大： 最近10天的平均成交量 > 过去60天平均成交量的 1.5倍。
    """
    def check_bottom_volume(df_stock):
        """
        检查底部放量
        """
        # 1. 判断位置 (Price Rank)
        current_price = df_stock['close'].iloc[-1]
        high_250 = df_stock['close'].rolling(250).max().iloc[-1]
        low_250 = df_stock['close'].rolling(250).min().iloc[-1]
        
        # 计算当前价格在过去一年中的位置 (0-1之间)
        price_position = (current_price - low_250) / (high_250 - low_250)
        
        # 2. 判断量能 (Volume Ratio)
        vol_ma10 = df_stock['vol'].rolling(10).mean().iloc[-1]
        vol_ma60 = df_stock['vol'].rolling(60).mean().iloc[-1]
        
        volume_ratio = vol_ma10 / vol_ma60
        
        # 判定：位置低 (<30%水位) 且 放量 (>1.5倍)
        if price_position < 0.3 and volume_ratio > 1.5:
            return True, f"底部堆量: 位置{price_position:.2f}, 量比{volume_ratio:.2f}"
            
        return False, "非底部堆量形态"

    """
    5. 综合选股脚本 (把它们串起来)
    这是一个简单的整合逻辑，实际使用时你可以遍历整个A股列表。
    """
    def analyze_stock_main_force(self, stock_code, df_price, df_holders, df_index):
        print(f"正在分析股票: {stock_code} ...")
        
        score = 0
        reasons = []
        
        # 1. 检查筹码
        is_concentrated, msg1 = self.check_chip_concentration(df_holders)
        if is_concentrated:
            score += 1
            reasons.append(msg1)
            
        # 2. 检查抗跌性
        is_resilient, msg2 = self.check_resilience(df_price, df_index)
        if is_resilient:
            score += 1
            reasons.append(msg2)
            
        # 3. 检查控盘形态
        is_controlled, msg3 = self.check_small_bull_trend(df_price)
        if is_controlled:
            score += 1
            reasons.append(msg3)
            
        # 4. 检查底部放量
        is_bottom_vol, msg4 = self.check_bottom_volume(df_price)
        if is_bottom_vol:
            score += 1
            reasons.append(msg4)
        
        print(f"综合得分: {score}/4")
        if score >= 3:
            print("★ 发现疑似强庄股！")
            print("特征:", reasons)
        else:
            print("未发现明显主力特征")
            
    # 注意：你需要自己准备数据源 (df_price, df_holders, df_index) 传入上述函数才能运行完整分析。
from datetime import datetime
import time as time
from ConsolidationStockScreener import ConsolidationStockScreener
import mysql as mysql
import pandas as pd

def test_1():
    """
    主执行函数
    """
    # 初始化筛选器
    screener = ConsolidationStockScreener()
    
    print("开始筛选横盘股票...")
    now = datetime.now()
    t = now.strftime('%Y-%m-%d')
    start = now.strftime('%Y-%m-%d %H:%M:%S')
    print(f"{start} 开始，筛选条件: 横盘10-60天, 截止日期: {t}")

    # 执行筛选
    results = screener.find_consolidation_stocks(
        min_days=10,
        max_days=60,
        volatility_threshold=0.015
    )
    
    # 输出结果
    if not results.empty:
        print(f"\n找到 {len(results)} 只横盘股票:")
        print("=" * 100)
        
         # 保存结果到文件
        results.to_csv('D:\\工作文件夹\\consolidation_stocks_20251022.csv', index=False)
        print(f"\n完整结果已保存到: consolidation_stocks_20251022.csv")

        for idx, row in results.head(20).iterrows():
            print(f"股票: {row['stock_code']}")
            print(f"  横盘天数: {row['consolidation_days']}天")
            print(f"  横盘期间: {row['start_date'].date()} 至 {row['end_date'].date()}")
            print(f"  波动率: {row['volatility']:.4f}")
            print(f"  价格区间: {row['price_range_pct']:.2%}")
            print(f"  ATR相对波动: {row['atr_ratio']:.2%}")
            print(f"  成交量比率: {row['volume_ratio']:.2f}")
            print(f"  横盘评分: {row['consolidation_score']:.2f}")
            print("-" * 50)
        
        # 统计信息
        print(f"\n统计信息:")
        print(f"平均横盘天数: {results['consolidation_days'].mean():.1f}天")
        print(f"最长横盘: {results['consolidation_days'].max()}天")
        print(f"最短横盘: {results['consolidation_days'].min()}天")
        
        # 按横盘天数分组
        bins = [10, 20, 40, 80]
        labels = ['10-20天', '21-40天', '41-80天']
        results['period_group'] = pd.cut(results['consolidation_days'], bins=bins, labels=labels)
        
        group_counts = results['period_group'].value_counts().sort_index()
        print("\n横盘天数分布:")
        for group, count in group_counts.items():
            print(f"  {group}: {count}只股票")
            
    else:
        print("未找到符合条件的横盘股票")

def test_2():
    print("开始筛选横盘股票...")
    now = datetime.now()
    t = now.strftime('%Y-%m-%d')
    start = now.strftime('%Y-%m-%d %H:%M:%S')
    print(f"{start} 开始，筛选条件: 横盘30天, 截止日期: {t}")

     # 初始化筛选器
    screener = ConsolidationStockScreener()
    results = screener.find_consolidation_stocks_2(threshold=50)

    # 输出结果
    if not results.empty:
        print(f"\n找到 {len(results)} 只横盘股票:")
        print("=" * 100)
        
         # 保存结果到文件
        results.to_csv('D:\\工作文件夹\\consolidation_stocks_20251026.csv', index=False)
        print(f"\n完整结果已保存到: consolidation_stocks_20251026.csv")

        for idx, row in results.head(20).iterrows():
            print(f"股票: {row['stock_code']}")
            print(f"  价格区间涨幅: {row['price_range_pct']:.2%}")
            print(f"  价格区间振幅: {row['amplitude']:.2%}")
            print(f"  波动率: {row['volatility']:.4f}")
            print(f"  是否突破箱体: {row['break_out']}")
            print(f"  是否未连续三天上涨: {row['three_day_rise']}")
            print("-" * 50)
            
    else:
        print("未找到符合条件的横盘股票")

if __name__ == "__main__":
    # test_1()
    test_2()
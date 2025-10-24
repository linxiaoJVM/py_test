import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings("ignore")


class MultiFactorStockSelector:
    """
    多因子量化选股策略
    使用财务指标、技术指标和市场指标进行综合评分选股
    """

    def __init__(self):
        self.stock_list = []
        self.factor_data = pd.DataFrame()

    def get_all_stocks(self):
        """从JSON文件获取股票列表"""
        try:
            # 尝试多个可能的文件路径
            possible_paths = [
                "D:\电子书\量化代码\qmt_stock_list.json"
            ]

            json_file_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    json_file_path = path
                    print(f"找到股票数据文件: {path}")
                    break

            if json_file_path is None:
                print("错误：在以下路径中都找不到股票数据文件 qmt_stock_list.json:")
                for path in possible_paths:
                    print(f"  - {os.path.abspath(path)}")
                print("\n当前工作目录:", os.getcwd())
                print("脚本所在目录:", os.path.dirname(os.path.abspath(__file__)))

                # 列出当前目录和trade目录的文件
                print("\n当前目录文件:")
                try:
                    for file in os.listdir("."):
                        print(f"  - {file}")
                except:
                    pass

                if os.path.exists("trade"):
                    print("\ntrade目录文件:")
                    try:
                        for file in os.listdir("trade"):
                            print(f"  - {file}")
                    except:
                        pass

                print("\n请确保 qmt_stock_list.json 文件存在于正确的位置")
                return pd.DataFrame()

            with open(json_file_path, "r", encoding="utf-8") as f:
                stock_data = json.load(f)

            # 转换为DataFrame格式
            stock_list = []
            for stock in stock_data:
                stock_list.append(
                    {
                        "code": stock["InstrumentID"],
                        "name": stock["InstrumentName"],
                        "exchange": stock["ExchangeID"],
                        "pre_close": stock["PreClose"],
                        "up_stop_price": stock["UpStopPrice"],
                        "down_stop_price": stock["DownStopPrice"],
                        "is_trading": stock["IsTrading"],
                    }
                )

            self.stock_list = pd.DataFrame(stock_list)
            print(f"成功从JSON文件获取{len(self.stock_list)}只股票信息")
            return self.stock_list
        except FileNotFoundError as e:
            print(f"文件未找到错误: {e}")
            print("请检查文件路径是否正确")
            return pd.DataFrame()
        except json.JSONDecodeError as e:
            print(f"JSON文件格式错误: {e}")
            return pd.DataFrame()
        except Exception as e:
            print(f"获取股票列表失败: {e}")
            return pd.DataFrame()

    def get_financial_factors(self, stock_code):
        """获取财务因子数据（模拟数据）"""
        try:
            # 由于使用JSON数据，这里使用模拟的财务数据
            # 实际应用中可以从其他数据源获取真实财务数据
            np.random.seed(
                hash(stock_code) % 2**32
            )  # 使用股票代码作为随机种子，确保结果一致

            factors = {
                "pe_ratio": max(5, np.random.normal(15, 8)),  # PE比率，正态分布
                "pb_ratio": max(0.5, np.random.normal(2, 1)),  # PB比率
                "roe": max(0, np.random.normal(12, 6)),  # ROE，百分比
                "debt_ratio": max(0, min(100, np.random.normal(40, 15))),  # 资产负债率
            }
            return factors
        except Exception as e:
            print(f"获取{stock_code}财务数据失败: {e}")
            return {}

    def get_technical_factors(self, stock_code):
        """获取技术因子数据（基于JSON中的价格信息模拟）"""
        try:
            # 从stock_list中获取该股票的基础信息
            stock_info = self.stock_list[self.stock_list["code"] == stock_code]
            if stock_info.empty:
                return {}

            pre_close = stock_info.iloc[0]["pre_close"]
            up_stop = stock_info.iloc[0]["up_stop_price"]
            down_stop = stock_info.iloc[0]["down_stop_price"]

            # 使用股票代码生成一致的随机数据
            np.random.seed(hash(stock_code) % 2**32)

            # 模拟当前价格（在涨跌停范围内）
            current_price = np.random.uniform(down_stop * 1.02, up_stop * 0.98)

            # 模拟移动平均线
            ma5 = pre_close * np.random.uniform(0.98, 1.02)
            ma20 = pre_close * np.random.uniform(0.95, 1.05)

            factors = {
                "price_ma5_ratio": current_price / ma5,
                "price_ma20_ratio": current_price / ma20,
                "rsi": np.random.uniform(20, 80),  # RSI指标
                "volume_ratio": np.random.uniform(0.5, 2.0),  # 成交量比率
            }
            return factors
        except Exception as e:
            print(f"获取{stock_code}技术数据失败: {e}")
            return {}

    def calculate_factor_score(self, factors):
        """计算因子综合得分"""
        if not factors:
            return 0

        score = 0

        # 财务因子评分 (权重40%)
        # PE比率评分 (越低越好)
        pe_score = (
            max(0, 100 - factors.get("pe_ratio", 50))
            if factors.get("pe_ratio", 0) > 0
            else 0
        )

        # PB比率评分 (越低越好)
        pb_score = (
            max(0, 100 - factors.get("pb_ratio", 10) * 10)
            if factors.get("pb_ratio", 0) > 0
            else 0
        )

        # ROE评分 (越高越好)
        roe_score = (
            min(100, factors.get("roe", 0) * 5) if factors.get("roe", 0) > 0 else 0
        )

        # 负债率评分 (越低越好)
        debt_score = (
            max(0, 100 - factors.get("debt_ratio", 50))
            if factors.get("debt_ratio", 0) >= 0
            else 0
        )

        financial_score = (
            pe_score * 0.3 + pb_score * 0.3 + roe_score * 0.3 + debt_score * 0.1
        ) * 0.4

        # 技术因子评分 (权重60%)
        # 价格相对MA5评分
        ma5_score = min(100, max(0, (factors.get("price_ma5_ratio", 1) - 0.95) * 500))

        # 价格相对MA20评分
        ma20_score = min(100, max(0, (factors.get("price_ma20_ratio", 1) - 0.9) * 200))

        # RSI评分 (30-70为好区间)
        rsi = factors.get("rsi", 50)
        if 30 <= rsi <= 70:
            rsi_score = 100 - abs(rsi - 50) * 2
        else:
            rsi_score = max(0, 50 - abs(rsi - 50))

        # 成交量比率评分
        volume_score = min(100, max(0, (factors.get("volume_ratio", 1) - 0.8) * 100))

        technical_score = (
            ma5_score * 0.25
            + ma20_score * 0.25
            + rsi_score * 0.25
            + volume_score * 0.25
        ) * 0.6

        total_score = financial_score + technical_score
        return round(total_score, 2)

    def select_stocks(self, top_n=20):
        """执行选股策略"""
        print("开始执行多因子选股策略...")

        # 获取所有股票
        if self.stock_list is None or len(self.stock_list) == 0:
            self.get_all_stocks()

        if len(self.stock_list) == 0:
            print("未能获取股票列表")
            return pd.DataFrame()

        results = []

        # 处理所有股票
        sample_stocks = self.stock_list.copy()  # 处理所有股票
        # 按股票代码排序，确保处理顺序稳定
        sample_stocks = sample_stocks.sort_values("code").reset_index(drop=True)

        print(f"开始分析 {len(sample_stocks)} 只股票...")

        for idx, row in sample_stocks.iterrows():
            stock_code = row["code"]
            stock_name = row["name"]

            # 每处理100只股票显示一次进度
            if (idx + 1) % 100 == 0 or idx == 0:
                print(f"正在分析 {stock_code} - {stock_name} ({idx+1}/{len(sample_stocks)}) - 进度: {((idx+1)/len(sample_stocks)*100):.1f}%")

            # 获取各类因子数据
            financial_factors = self.get_financial_factors(stock_code)
            technical_factors = self.get_technical_factors(stock_code)

            # 合并所有因子
            all_factors = {**financial_factors, **technical_factors}

            if all_factors:
                score = self.calculate_factor_score(all_factors)

                result = {
                    "stock_code": stock_code,
                    "stock_name": stock_name,
                    "exchange": row["exchange"],
                    "score": score,
                    **all_factors,
                }
                results.append(result)

        print(f"分析完成！共分析了 {len(results)} 只股票")

        # 转换为DataFrame并按得分排序
        results_df = pd.DataFrame(results)
        if not results_df.empty:
            # 按得分降序排序，得分相同时按股票代码升序排序（确保结果稳定）
            results_df = results_df.sort_values(
                ["score", "stock_code"],
                ascending=[False, True]
            ).head(top_n)

        return results_df

    def display_results(self, results_df):
        """显示选股结果"""
        if results_df.empty:
            print("没有选出符合条件的股票")
            return

        print(f"\n=== 多因子选股结果 (Top {len(results_df)}) ===")
        print("-" * 80)

        for idx, row in results_df.iterrows():
            print(f"排名: {list(results_df.index).index(idx)+1}")
            print(f"股票代码: {row['stock_code']} ({row['exchange']})")
            print(f"股票名称: {row['stock_name']}")
            print(f"综合得分: {row['score']:.2f}")
            print(f"PE比率: {row.get('pe_ratio', 'N/A'):.2f}")
            print(f"PB比率: {row.get('pb_ratio', 'N/A'):.2f}")
            print(f"ROE: {row.get('roe', 'N/A'):.2f}%")
            print(f"RSI: {row.get('rsi', 'N/A'):.2f}")
            print(f"价格/MA5比率: {row.get('price_ma5_ratio', 'N/A'):.3f}")
            print(f"价格/MA20比率: {row.get('price_ma20_ratio', 'N/A'):.3f}")
            print("-" * 40)


def main():
    """主函数"""
    print("=== A股多因子量化选股系统 ===")

    # 设置全局随机种子，确保每次运行结果一致
    np.random.seed(42)

    # 创建选股器实例
    selector = MultiFactorStockSelector()

    # 执行选股
    selected_stocks = selector.select_stocks(top_n=10)

    # 显示结果
    selector.display_results(selected_stocks)

    print(f"\n选股完成，共选出 {len(selected_stocks)} 只股票")


if __name__ == "__main__":
    main()

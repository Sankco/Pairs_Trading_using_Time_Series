import warnings
import pandas as pd
import yfinance as yf
import time
from datetime import datetime, timedelta


class YahooDataSource:

    def __init__(self, start_date, end_date, tickers, columns):
        self.tickers = tickers
        self.columns = columns
        self.start_date = start_date
        self.end_date = end_date
        self.data = self.get_yahoo_data()

    def get_yahoo_data(self):
        data = {}
        failed_symbols = []
        
        print(f"正在获取 {len(self.tickers)} 个股票的数据，时间范围：{self.start_date} 到 {self.end_date}")
        
        for i, symbol in enumerate(self.tickers):
            try:
                print(f"获取 {symbol} 数据 ({i+1}/{len(self.tickers)})...")
                
                # 添加延迟避免频率限制
                if i > 0:
                    time.sleep(0.2)
                
                ticker = yf.Ticker(symbol)
                
                # 转换日期格式
                start_str = self.start_date.strftime('%Y-%m-%d') if isinstance(self.start_date, datetime) else self.start_date
                end_str = self.end_date.strftime('%Y-%m-%d') if isinstance(self.end_date, datetime) else self.end_date
                
                hist = None
                
                # 尝试多种方法获取数据
                # 方法1: 使用更新的参数
                try:
                    hist = ticker.history(
                        start=start_str, 
                        end=end_str, 
                        interval="1d",
                        auto_adjust=True,
                        prepost=True,
                        threads=True,
                        proxy=None
                    )
                except Exception as e1:
                    print(f"  方法1失败: {e1}")
                    
                    # 方法2: 分段获取数据（避免时间范围过长的问题）
                    try:
                        hist = self._get_data_in_chunks(ticker, start_str, end_str)
                    except Exception as e2:
                        print(f"  方法2失败: {e2}")
                        
                        # 方法3: 使用period参数
                        try:
                            # 计算大概的时间长度
                            start_dt = datetime.strptime(start_str, '%Y-%m-%d')
                            end_dt = datetime.strptime(end_str, '%Y-%m-%d')
                            days_diff = (end_dt - start_dt).days
                            
                            if days_diff > 365 * 5:  # 超过5年用max
                                period = "max"
                            elif days_diff > 365 * 2:  # 超过2年用5y
                                period = "5y"
                            elif days_diff > 365:  # 超过1年用2y
                                period = "2y"
                            else:
                                period = "1y"
                            
                            hist = ticker.history(period=period)
                            
                            # 过滤到指定日期范围
                            if hist is not None and not hist.empty:
                                hist = hist[start_str:end_str]
                        except Exception as e3:
                            print(f"  方法3失败: {e3}")
                
                if hist is not None and not hist.empty:
                    hist.reset_index(inplace=True)
                    print(f"  成功获取 {len(hist)} 条记录")
                    
                    # 检查并存储数据
                    for col in self.columns:
                        if col in hist.columns:
                            data[symbol + "_" + col] = hist[col].to_numpy()
                        else:
                            print(f"  警告: 列 {col} 不存在于 {symbol} 的数据中")
                            print(f"  可用列: {hist.columns.tolist()}")
                else:
                    failed_symbols.append(symbol)
                    print(f"  无法获取 {symbol} 的数据")
                    
            except Exception as e:
                failed_symbols.append(symbol)
                print(f"获取 {symbol} 数据时出错: {type(e).__name__}: {e}")

        if failed_symbols:
            print(f"\n无法获取以下 {len(failed_symbols)} 个股票的数据: {failed_symbols}")
        
        successful_symbols = len(data) // len(self.columns) if len(self.columns) > 0 else 0
        print(f"\n成功获取 {successful_symbols} 个股票的数据")
        return data
    
    def _get_data_in_chunks(self, ticker, start_str, end_str, chunk_years=2):
        """分段获取数据以避免时间范围过长的问题"""
        start_dt = datetime.strptime(start_str, '%Y-%m-%d')
        end_dt = datetime.strptime(end_str, '%Y-%m-%d')
        
        all_data = []
        current_start = start_dt
        
        while current_start < end_dt:
            current_end = min(current_start + timedelta(days=365 * chunk_years), end_dt)
            
            chunk_start_str = current_start.strftime('%Y-%m-%d')
            chunk_end_str = current_end.strftime('%Y-%m-%d')
            
            try:
                chunk_data = ticker.history(start=chunk_start_str, end=chunk_end_str)
                if not chunk_data.empty:
                    all_data.append(chunk_data)
            except Exception as e:
                print(f"    获取 {chunk_start_str} 到 {chunk_end_str} 的数据失败: {e}")
            
            current_start = current_end + timedelta(days=1)
            time.sleep(0.1)  # 添加小延迟
        
        if all_data:
            combined_data = pd.concat(all_data)
            combined_data = combined_data[~combined_data.index.duplicated(keep='first')]
            combined_data.sort_index(inplace=True)
            return combined_data
        else:
            return pd.DataFrame()
    
    def get_data_by_column_tickers(self, columns=-1, tickers=-1):
        all_tickers = self.tickers
        all_columns = self.columns

        if columns == -1:
            columns = all_columns
        
        if tickers == -1:
            tickers = all_tickers
        
        validated_tickers = set(tickers).intersection(all_tickers)
        validated_columns = set(columns).intersection(all_columns)

        if len(set(tickers)) != len(set(validated_tickers)):
            warnings.warn(f"以下股票代码未找到: {set(tickers)-set(validated_tickers)}")
        
        if len(set(columns)) != len(set(validated_columns)):
            warnings.warn(f"以下列未找到: {set(columns)-set(validated_columns)}")
        
        ticker_columns = self.create_ticker_columns(validated_columns, validated_tickers)

        # 只包含实际存在的列
        available_columns = {key: self.data[key] for key in ticker_columns if key in self.data}
        
        if len(available_columns) != len(ticker_columns):
            missing = set(ticker_columns) - set(available_columns.keys())
            print(f"警告: 缺少以下数据列: {missing}")

        return pd.DataFrame(available_columns)
    
    def create_ticker_columns(self, columns, tickers):
        ticker_columns = []
        for tick in tickers:
            for col in columns:
                name = tick + "_" + col
                ticker_columns.append(name)
        return ticker_columns
    
    def get_tickers(self, ticker_columns):
        return [i.split("_")[0] for i in ticker_columns]

    

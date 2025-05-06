from core import DataFeed
from typing import Optional
import pandas as pd
import yfinance as yf

class PandasDataFeed(DataFeed):
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.idx = 0

    def get_next(self) -> Optional[pd.Series]:
        if self.idx >= len(self.df):
            return None
        row = self.df.iloc[self.idx]
        self.idx += 1
        return row

class YahooFinanceDataFeed(DataFeed):
    def __init__(self, ticker: str, start: str, end: str, interval: str = "1d"):
        self.df = yf.download(ticker, start=start, end=end, interval=interval)
        self.df.index = pd.to_datetime(self.df.index)
        self.df.columns = [c[0].lower() for c in self.df.columns]
        self.df["symbol"] = ticker
        self.idx = 0

    def get_next(self) -> Optional[pd.Series]:
        if self.idx >= len(self.df):
            return None
        row = self.df.iloc[self.idx]
        row.name = self.df.index[self.idx]  # ensure timestamp is accessible
        self.idx += 1
        return row
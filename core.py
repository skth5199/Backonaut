import pandas as pd
from abc import ABC, abstractmethod
from typing import Optional, List

class Order:
    def __init__(self, symbol: str, quantity: int, price: float, side: str, timestamp: pd.Timestamp):
        assert side in ("buy", "sell")
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.side = side
        self.timestamp = timestamp

class Trade:
    def __init__(self, order: Order):
        self.symbol = order.symbol
        self.quantity = order.quantity
        self.price = order.price
        self.side = order.side
        self.timestamp = order.timestamp
        self.pnl = 0.0

class Portfolio:
    def __init__(self, cash: float):
        self.cash = cash
        self.positions = {}  # symbol -> quantity
        self.trades: List[Trade] = []

    def execute_order(self, order: Order):
        cost = order.quantity * order.price
        if order.side == "buy":
            self.cash -= cost
            self.positions[order.symbol] = self.positions.get(order.symbol, 0) + order.quantity
        elif order.side == "sell":
            self.cash += cost
            self.positions[order.symbol] = self.positions.get(order.symbol, 0) - order.quantity
        self.trades.append(Trade(order))

    def net_liquidation(self, prices: dict):
        # TODO: Add support for multiple symbols
        equity = self.cash
        for dt, qty in self.positions.items():
            equity += qty * list(prices.values())[0]
        return equity
    
class Strategy(ABC):
    @abstractmethod
    def on_data(self, data: pd.Series) -> Optional[Order]:
        pass

class DataFeed(ABC):
    @abstractmethod
    def get_next(self) -> Optional[pd.Series]:
        pass
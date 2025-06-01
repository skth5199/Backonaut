import pandas as pd
from typing import Optional
from core import Order, Strategy

class MovingAverageCrossStrategy(Strategy):
    def __init__(self, short_window=5, long_window=20):
        self.prices = []
        self.short_window = short_window
        self.long_window = long_window
        self.position = 0  # 0 = flat, 1 = long

    def on_data(self, data: pd.Series) -> Optional[Order]:
        self.prices.append(data['close'])
        if len(self.prices) < self.long_window:
            return None

        short_ma = pd.Series(self.prices[-self.short_window:]).mean()
        long_ma = pd.Series(self.prices[-self.long_window:]).mean()

        # Todo: Remove quantity hardcoding, check for crossover signals
        if short_ma > long_ma and self.position == 0:
            self.position = 1
            return Order(symbol=data.name, quantity=100, price=data['close'], side="buy", timestamp=data.name)
        elif short_ma < long_ma and self.position == 1:
            self.position = 0
            return Order(symbol=data.name, quantity=100, price=data['close'], side="sell", timestamp=data.name)

        return None
    
class ThreeDayDownStrategy(Strategy):
    def __init__(self, recurring_trade_amount=100):
        self.recurring_trade_amount = recurring_trade_amount
        self.last_prices = []
        self.symbol = None  # to store the symbol name
        self.position = 0   # not used for exits in this strategy

    def on_data(self, data: pd.Series) -> Optional[Order]:
        close = data['close']
        self.last_prices.append(close)
        self.symbol = data.name  # assuming data.name holds the symbol or timestamp

        # Keep only last 3 closes
        if len(self.last_prices) > 3:
            self.last_prices.pop(0)

        if len(self.last_prices) < 3:
            return None

        # Check if we have 3 consecutive down closes
        if (self.last_prices[-3] > self.last_prices[-2] > self.last_prices[-1]):
            # BUY £100 worth of stock
            price = close
            quantity = self.recurring_trade_amount / price
            if quantity == 0:
                return None  # skip if price is too high
            self.last_prices = [close]  # reset price history
            return Order(symbol=self.symbol, quantity=quantity, price=price, side="buy", timestamp=data.name)

        return None
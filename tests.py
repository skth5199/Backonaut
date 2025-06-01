import unittest
import pandas as pd
from core import Order, Portfolio, Trade, Strategy, DataFeed
from strategy import MovingAverageCrossStrategy, ThreeDayDownStrategy
from datafeeds import PandasDataFeed
from engine import BacktestEngine

class DummyStrategy(Strategy):
    """A simple strategy for testing: buys on first bar, sells on second."""
    def __init__(self):
        self.counter = 0

    def on_data(self, data: pd.Series):
        self.counter += 1
        if self.counter == 1:
            return Order(symbol="TEST", quantity=1, price=data['close'], side="buy", timestamp=data.name)
        elif self.counter == 2:
            return Order(symbol="TEST", quantity=1, price=data['close'], side="sell", timestamp=data.name)
        return None

class TestBackonaut(unittest.TestCase):
    def setUp(self):
        # Create a simple DataFrame for testing
        self.df = pd.DataFrame({
            "open": [100, 101, 102],
            "high": [101, 102, 103],
            "low": [99, 100, 101],
            "close": [100, 101, 102],
            "volume": [1000, 1100, 1200]
        }, index=pd.date_range("2024-01-01", periods=3))
        self.feed = PandasDataFeed(self.df)

    def test_order_execution(self):
        portfolio = Portfolio(1000)
        order = Order(symbol="TEST", quantity=2, price=100, side="buy", timestamp=pd.Timestamp("2024-01-01"))
        portfolio.execute_order(order)
        self.assertEqual(portfolio.positions["TEST"], 2)
        self.assertAlmostEqual(portfolio.cash, 800)

    def test_trade_recording(self):
        portfolio = Portfolio(1000)
        order = Order(symbol="TEST", quantity=1, price=100, side="buy", timestamp=pd.Timestamp("2024-01-01"))
        portfolio.execute_order(order)
        self.assertEqual(len(portfolio.trades), 1)
        self.assertIsInstance(portfolio.trades[0], Trade)

    def test_backtest_engine_run(self):
        strategy = DummyStrategy()
        engine = BacktestEngine(strategy, PandasDataFeed(self.df), initial_cash=1000)
        engine.run()
        history = engine.get_history()
        self.assertEqual(len(history), 3)
        # After buy and sell, position should be 0
        last_positions = history.iloc[-1]["positions"]
        self.assertEqual(last_positions.get("TEST", 0), 0)

    def test_moving_average_cross_strategy(self):
        strategy = MovingAverageCrossStrategy(short_window=1, long_window=2)
        feed = PandasDataFeed(self.df)
        orders = []
        for _ in range(len(self.df)):
            data = feed.get_next()
            order = strategy.on_data(data)
            if order:
                orders.append(order)
        # Should generate a buy and a sell order
        self.assertTrue(any(o.side == "buy" for o in orders))
        self.assertTrue(not any(o.side == "sell" for o in orders))

    def test_three_day_down_strategy(self):
        # Create a downtrend for 3 days
        df = pd.DataFrame({
            "open": [100, 99, 98],
            "high": [101, 100, 99],
            "low": [99, 98, 97],
            "close": [100, 99, 98],
            "volume": [1000, 1100, 1200]
        }, index=pd.date_range("2024-01-01", periods=3))
        strategy = ThreeDayDownStrategy(recurring_trade_amount=100)
        feed = PandasDataFeed(df)
        orders = []
        for _ in range(len(df)):
            data = feed.get_next()
            order = strategy.on_data(data)
            if order:
                orders.append(order)
        # Should generate a buy order after 3 down closes
        self.assertTrue(any(o.side == "buy" for o in orders))

if __name__ == "__main__":
    unittest.main()
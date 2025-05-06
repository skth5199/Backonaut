from engine import BacktestEngine
from datafeeds import PandasDataFeed, YahooFinanceDataFeed
from strategy import MovingAverageCrossStrategy

### Backtest a simple moving average crossover strategy using sample data
# # Load sample data
# df = pd.read_csv("//Users//sri//Desktop//Projects//Backonaut//AAPL.csv", index_col="Date", parse_dates=True)

# # Instantiate components
# feed = PandasDataFeed(df)
# strategy = MovingAverageCrossStrategy(short_window=5, long_window=20)
# engine = BacktestEngine(strategy, feed)

# # Run backtest
# engine.run()
# history = engine.get_history()
# print(history.tail())

### Backtesting the Thee day down strategy using Yahoo Finance data
# # Instantiate components
feed = YahooFinanceDataFeed(ticker="^GSPC", start="2023-01-01", end="2024-01-01", interval="1d")
strategy = MovingAverageCrossStrategy(short_window=5, long_window=20)
engine = BacktestEngine(strategy, feed)
# # Run backtest
engine.run()
history = engine.get_history()
print(history.tail())
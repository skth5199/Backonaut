
# 🧪 Backonaut: A Lightweight Backtesting Engine

**Backonaut** is a minimal, extensible Python backtesting engine for testing trading strategies on historical data.

## 🚀 Features

- Modular OOP architecture (strategy, data feed, portfolio)
- Supports custom strategies
- Works with Yahoo Finance via `yfinance`
- Tracks NAV, cash, and positions over time
- Generates PDF performance reports

## 📦 Project Structure

```
.
├── Backonaut/
│   ├── __init__.py
│   ├── core.py            # Core classes: Order, Trade, Portfolio, Strategy, DataFeed
│   ├── data.py            # Data feed implementations (e.g., YahooFinanceDataFeed)
│   ├── engine.py          # BacktestEngine: runs the backtest loop
│   ├── reporting.py       # Generates PDF reports with NAV chart and performance metrics
│   ├── strategy.py        # Example and base strategy classes
│   └── utils.py           # Utility functions (if present)
├── main.py                # Run backtests with chosen strategy and data
├── requirements.txt       # Required packages
├── README.md              # Project documentation
```

## 📈 Quickstart

```bash
pip install -r requirements.txt
```

```python
from core import *
from strategy import ThreeDayDownStrategy
from data import YahooFinanceDataFeed
from reporting import generate_pdf_report

feed = YahooFinanceDataFeed("AAPL", start="2023-01-01", end="2024-01-01")
strategy = ThreeDayDownStrategy()
engine = BacktestEngine(strategy, feed)
engine.run()

history = engine.get_history()
generate_pdf_report(history)
```

## 📊 Output

- **NAV Curve**
- **Performance Metrics**
- **Holdings Over Time**
- **PDF Report**

## 🧠 Customize

Plug in your own:
- Strategy logic
- Data feeds (CSV, API, etc.)
- Reporting style or dashboards

## 📃 License

MIT

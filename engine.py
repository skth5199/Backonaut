import pandas as pd
from core import Order, Portfolio, Strategy, DataFeed

class BacktestEngine:
    def __init__(self, strategy: Strategy, data_feed: DataFeed, initial_cash: float = 100_000):
        self.strategy = strategy
        self.data_feed = data_feed
        self.portfolio = Portfolio(initial_cash)
        self.history = []

    def run(self):
        while True:
            data = self.data_feed.get_next()
            if data is None:
                break

            order = self.strategy.on_data(data)
            if order:
                self.portfolio.execute_order(order)

            prices = {data.name: data['close']}
            nav = self.portfolio.net_liquidation(prices)
            self.history.append({
                'timestamp': data.name,
                'nav': nav,
                'cash': self.portfolio.cash,
                'positions': dict(self.portfolio.positions),
            })

    def get_history(self) -> pd.DataFrame:
        return pd.DataFrame(self.history).set_index('timestamp')
    
    # TODO: Modify this to work by date rather than by last date
    def get_net_worth(self) -> float:
        last_date_price = self.data_feed.df.iloc[-1]['close']
        equity = self.portfolio.cash + sum(self.portfolio.positions.values()) * last_date_price
        return equity
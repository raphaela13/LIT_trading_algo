from LIT_trading_algo import *
from datetime import datetime, timedelta

# backtest on mt5  for GBPUSD referring to backtesting validation part in paper
# will return dataframe backtesting.py table and graph

initialize_mt()

# Variables inputs

pair = 'GBPUSD'
rr = 2
buffer = 0.0
speed_factor = 1
start = datetime(2024, 4, 9) + timedelta(hours=2)
end = datetime(2024, 4, 9) + timedelta(hours=14)


print(backtest_asia_range_graph(pair, start, end, rr, buffer, speed_factor))


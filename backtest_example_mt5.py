from LIT_trading_algo import *
from datetime import datetime, timedelta

# 4 following sections allow to backtest between 1.6.23 until 27.4.24 on data extracted from Metatrader
# each pair with optimized variables
# return table results from backtesting.py and open backtest result graph on webpage

initialize_mt()

# Variables inputs

pair = 'USDCHF'
rr = 2
buffer = 0.0
speed_factor = 1
start = datetime(2024, 4, 1)
end = datetime(2024, 4, 27)

print(backtest(pair, start, end, rr, buffer, speed_factor))
print(backtest_asia_range_graph(pair, start, end, rr, buffer, speed_factor))


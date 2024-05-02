from LIT_trading_algo import *

import pandas as pd
pd.set_option('display.max_columns', None)  # Show all columns

# 4 following sections allow to backtest on csv files from 1.6.23 until 27.4.24
# each pair with optimized variables
# will return dataframe table with key elements, backtesting.py table and graph

m5_EURUSD = pd.read_csv("EURUSD_backtesting_data", parse_dates=['time'])
x = backtest_csv('EURUSD', 6, 0.0004, 0.9, m5_EURUSD)

# m5_GBPUSD = pd.read_csv("GBPUSD_backtesting_data", parse_dates=['time'])
# x = backtest_csv('GBPUSD', 6, 0.0002, 1.1, m5_GBPUSD)s

# m5_USDJPY = pd.read_csv("USDJPY_backtesting_data", parse_dates=['time'])
# x = backtest_csv('USDJPY', 1, 0.00, 0.9, m5_USDJPY)

# m5_USDCHF = pd.read_csv("USDCHF_backtesting_data", parse_dates=['time'])
# x = backtest_csv('USDCHF', 5, 0.0004, 1.2, m5_USDCHF)

print(x[0])
print(x[1])



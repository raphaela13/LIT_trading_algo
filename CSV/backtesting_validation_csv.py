from LIT_trading_algo import *

import pandas as pd
pd.set_option('display.max_columns', None)  # Show all columns

# backtest on csv files for GBPUSD referring to backtesting validation part in paper
# will return dataframe table with key elements, backtesting.py table and graph

m5 = pd.read_csv("backtesting_validation", parse_dates=['time'])
x = backtest_csv('GBPUSD', 2, 0.0, 1, m5)

print(x[0])
print(x[1])
from LIT_trading_algo import *

import pandas as pd
pd.set_option('display.max_columns', None)  # Show all columns

# backtest on csv files for USDCHF from 1.4.23 until 26.4.24 for the example in backtest_asia_range() example
# will return dataframe table with key elements, backtesting.py table and graph

m5 = pd.read_csv("USDCHF_backtesting_example", parse_dates=['time'])
x = backtest_csv('USDCHF', 2, 0.0, 1, m5)

print(x[0])
print(x[1])
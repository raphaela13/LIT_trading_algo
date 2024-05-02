from LIT_trading_algo.backtest.backtest_asia_range_csv import *

import pandas as pd


def backtest_csv(pair, rr, buffer, speed_factor, df):
    pd.set_option('display.max_columns', None)  # Show all columns

    x = backtest_asia_range_csv(pair, rr, buffer, speed_factor, df)

    result_backtest = pd.DataFrame(columns = ['symbol', 'Percentage wins', 'Number trades', 'Expected return', 'RR', 'buffer', 'speed factor'])
    new_row = pd.DataFrame([{'symbol': x[0], 'Percentage wins': x[1],
                         'Number trades': x[2], 'Expected return': x[3],
                         'RR': rr, 'buffer': buffer, 'speed factor': speed_factor}])
    result_backtest = result_backtest.dropna(how='all')
    result_backtest = result_backtest.dropna(axis=1, how='all')
    result_backtest = pd.concat([result_backtest, new_row], ignore_index=True)

    return [result_backtest, x[4]]
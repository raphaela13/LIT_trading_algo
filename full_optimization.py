from LIT_trading_algo import *
import MetaTrader5 as mt
from datetime import datetime, timedelta
import time
import pandas as pd
import numpy as np

start_time = time.time()

initialize_mt()
pd.set_option('display.max_columns', None)  # Show all columns

result_backtest_loop = pd.DataFrame(
    columns=['symbol', 'Percentage wins', 'Number trades', 'Expected return', 'RR', 'buffer', 'speed factor'])
pairs = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF']

for pair in pairs:

    list_max_return = []
    max_return = -100000
    rr = 0
    buffer = 0
    speed_factor = 0

    for i in np.arange(1, 7, 1):  # RR - 6x
        for y in np.arange(0.00, 0.0012, 0.0002):  # buffer - 6x
            for z in np.arange(0.9, 1.45, 0.1):  # speed factor - 6x

                x = backtest_asia_range(pair, datetime(2023, 6, 1), datetime(2024, 4, 27), i, y, z)
                if (x[3] > max_return):
                    list_max_return = x
                    max_return = x[3]
                    rr = i
                    buffer = y
                    speed_factor = z

    new_row = pd.DataFrame([{'symbol': list_max_return[0], 'Percentage wins': list_max_return[1],
                             'Number trades': list_max_return[2], 'Expected return': list_max_return[3],
                             'RR': rr, 'buffer': buffer, 'speed factor': speed_factor}])
    result_backtest_loop = pd.concat([result_backtest_loop, new_row], ignore_index=True)

print("--- %s seconds ---" % (time.time() - start_time))
print(result_backtest_loop)

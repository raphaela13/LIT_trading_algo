from LIT_trading_algo import *
from datetime import datetime

# 4 following sections allow to backtest between 1.6.23 until 27.4.24 on data extracted from Metatrader
# each pair with optimized variables
# print results with the following dataframe format: ['symbol', 'Percentage wins', 'Number trades',
#                                                     'Expected return', 'RR', 'buffer', 'speed factor']

pair = 'EURUSD'
rr = 6
buffer = 0.0004
speed_factor = 0.9
start = datetime(2023, 6, 1)
end = datetime(2024, 4, 28)

# pair = 'GBPUSD'
# rr = 6
# buffer = 0.0002
# speed_factor = 1.1
# start = datetime(2023, 6, 1)
# end = datetime(2024, 4, 28)

# pair = 'USDJPY'
# rr = 1
# buffer = 0.0
# speed_factor = 0.9
# start = datetime(2023, 6, 1)
# end = datetime(2024, 4, 28)

# pair = 'USDCHF'
# rr = 5
# buffer = 0.0004
# speed_factor = 1.2
# start = datetime(2023, 6, 1)
# end = datetime(2024, 4, 28)


print(backtest(pair, start, end, rr, buffer, speed_factor))
from LIT_trading_algo import *
import MetaTrader5 as mt
from datetime import datetime, timedelta
import time
import pandas as pd
import numpy as np
from backtesting import Backtest, Strategy

initialize_mt()

# list of pairs four major forex pairs

pairs = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF']
prefix = 'AR_'

# creating list of variables for each pair

for i in pairs:
    variable_name = prefix + i
    globals()[variable_name] = reset_variables(i)  # Create and assign value

# while loop between 7am and 11:59pm

while (7 <= datetime.now().hour <= 11):

    # resetting list at 11:59am

    if (datetime.now().hour == 11) & (datetime.now().minute == 59):
        for i in pairs:
            variable_name = prefix + i
            globals()[variable_name] = reset_variables(i)  # Create and assign value
            print(f'reset for {i}')

    # collecting asia range for each pairs at 7am

    if (datetime.now().hour == 7) & (datetime.now().minute == 33):
        AR_EURUSD[1] = collect_Asia_Range(AR_EURUSD[0])
        AR_GBPUSD[1] = collect_Asia_Range(AR_GBPUSD[0])
        AR_USDJPY[1] = collect_Asia_Range(AR_USDJPY[0])
        AR_USDCHF[1] = collect_Asia_Range(AR_USDCHF[0])
        print(f'EURUSD: {AR_EURUSD[1]} - GBPUSD: {AR_GBPUSD[1]} - USDJPY: {AR_USDJPY[1]} - USDCHF: {AR_USDCHF[1]} ')

    # running Asia_Range_Setup

    # fill in the last 4 desired arguments for each pair: rr, buffer, speed_factor, risk

    AR_EURUSD = asia_range_setup(AR_EURUSD, 6, 0.0004, 0.9, 0.01)
    AR_GBPUSD = asia_range_setup(AR_GBPUSD, 6, 0.0004, 1.1, 0.01)
    AR_USDJPY = asia_range_setup(AR_USDJPY, 1, 0.00, 0.9, 0.01)
    AR_USDCHF = asia_range_setup(AR_USDCHF, 5, 0.0004, 1.2, 0.01)

    # make code run each 5 minutes (300 seconds)

    time.sleep(300)


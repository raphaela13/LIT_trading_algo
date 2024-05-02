# LIT_trading_algo

## Capstone project for Advanced programming 
author: Raphael Arguello

University of Lausanne

raphael.arguello@unil.ch

### Research question: 
How can the Liquidity Inducement Theorem (LIT) be effectively implemented for both backtesting and real-time trading using Python?

## to import the package: 
from LIT_trading_algo import *

## Description:
Package allowing to execute the algorithm on a live Metatrader 5 account, as well as backtesting the strategy on historical data.

## Main code to run the live algorithm, example for EURUSD: 

```python

initialize_mt()
AR_EURUSD = reset_variables('EURUSD')

while (7 <= datetime.now().hour <= 11):

  if (datetime.now().hour == 11) & (datetime.now().minute == 59):
    AR_EURUSD = reset_variables('EURUSD')
      
  if (datetime.now().hour == 7) & (datetime.now().minute == 15):
      AR_EURUSD[1] = collect_Asia_Range(AR_EURUSD[0])
      
    # fill in the last 4 desired arguments for each pair: rr, buffer, speed_factor, risk
  AR_EURUSD = asia_range_setup(AR_EURUSD, 6, 0.0004, 0.9, 0.01)

  time.sleep(300)

```

---------------------

## Main code to run the backtesting, example for EURUSD: 

```python


# print results with the following dataframe format: ['symbol', 'Percentage wins', 'Number trades',
#                                                     'Expected return', 'RR', 'buffer', 'speed factor']

pair = 'EURUSD'
rr = 6
buffer = 0.0004
speed_factor = 0.9
start = datetime(2023, 6, 1)
end = datetime(2024, 4, 28)

print(backtest(pair, start, end, rr, buffer, speed_factor))
```
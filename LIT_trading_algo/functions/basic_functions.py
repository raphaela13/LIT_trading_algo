import MetaTrader5 as mt
from datetime import datetime, timedelta
import pandas as pd



# Def function for bull and bear candle
# argument is dataframe row of specific candle

def bear(candle):
    if candle.iloc[4] < candle.iloc[1]:
        return True
    else:
        return False


def bull(candle):
    if candle.iloc[1] < candle.iloc[4]:
        return True
    else:
        return False


# function finding last low and high based on number of last candles
# do as it check the low from 7am

def last_low(df, n):
    low = 500000

    for i in range(n):
        if df.iloc[-i - 1].iloc[3] < low:
            low = df.iloc[-i - 1].iloc[3]
    return low


def last_high(df, n):
    high = 0
    for i in range(n):
        if df.iloc[-i - 1].iloc[2] > high:
            high = df.iloc[-i - 1].iloc[2]
    return high


# format of list AR = [Asia high, low of extreme candle AH, High of extreme candle AL, Asia Low]
# time on table is time of the broker. Using M15 as need M15 POI reaction to enter trade

def collect_Asia_Range(symbol):
    asia_session = pd.DataFrame(mt.copy_rates_range(symbol, mt.TIMEFRAME_M15,
                                                    datetime.now() - timedelta(hours=6),
                                                    datetime.now() + timedelta(hours=3)))
    AR = []
    AH = asia_session.high.max()
    AL = asia_session.low.min()
    AR += [asia_session.high.max()]
    AR += [asia_session[asia_session['high'] == AH].low.values[0]]
    AR += [asia_session[asia_session['low'] == AL].high.values[0]]
    AR += [asia_session.low.min()]

    return AR


# argument is the symbol name

def reset_variables(symbol):
    AR = []
    AH_grab = False
    Reaction_AH = False
    AH_Close_POI = False
    Sell_AH_taken = False
    Time_AH_grab = 0
    Max_AH_time = 0

    AL_grab = False
    Reaction_AL = False
    AL_Close_POI = False
    Buy_AL_taken = False
    Time_AL_grab = 0
    Max_AL_time = 0

    return [symbol, AR, AH_grab, Reaction_AH, AH_Close_POI, Sell_AH_taken, Time_AH_grab, Max_AH_time,
            AL_grab, Reaction_AL, AL_Close_POI, Buy_AL_taken, Time_AL_grab, Max_AL_time]


# Speed function definition:
# arguments (df, total number of candle to test, last number of candle to test for change speed, speed factor)
# Speed here defined in candle length

def speed(df, num_candle, num_candle_speed, speed_factor):
    speed_avg = 0
    speed_avg_last = 0
    speed_total = 0
    speed_total_last = 0

    for i in range(num_candle):
        speed_total += abs(df.iloc[-i - 1 - num_candle_speed].iloc[2] - df.iloc[-i - 1 - num_candle_speed].iloc[3])
    speed_avg = speed_total / num_candle

    for i in range(num_candle_speed):
        speed_total_last += abs(df.iloc[-i - 1].iloc[2] - df.iloc[-i - 1].iloc[3])
    speed_avg_last = speed_total_last / num_candle_speed

    if speed_avg_last >= speed_avg * speed_factor:
        return True
    else:
        return False


# Metatrader5 login
def initialize_mt():
    try:

        login = 51848565
        password = '514A!u$aEA2@Nr'
        server = 'ICMarketsSC-Demo'

        mt.initialize()
        mt.login(login, password, server)
        print('Successfully connected to account')
    except Exception as e:
        print('Failed to connect to trading account')
        print(e)

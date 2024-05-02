from LIT_trading_algo.functions import *
import MetaTrader5 as mt
from datetime import timedelta
import pandas as pd
from backtesting import Backtest, Strategy


# return [% wins, # trades]

def backtest_asia_range_csv(symbol, rr, buffer, speed_factor, df):
    # Collection M5 data for the period entered as argument
    m5 = df

    # defining variables which will allow the execution of trades

    AH_grab = False
    Reaction_AH = False
    AH_Close_POI = False
    Take_Sell_AH = False
    Sell_AH_taken = False
    Time_AH_grab = 0
    Max_AH_time = 0

    AL_grab = False
    Reaction_AL = False
    AL_Close_POI = False
    Take_Buy_AL = False
    Buy_AL_taken = False
    Time_AL_grab = 0
    Max_AL_time = 0

    # defining the following list: AR =[Asia range data], signal = [1 for buys, 2 for sells], sl = [price level for sl], tp = [price level for tp]

    AR = []
    signal = [0] * len(m5)
    sl = [0] * len(m5)
    tp = [0] * len(m5)

    # Loop through all the dataset
    # ndf allow to create a new data frame containing the data from the start up to index n+1
    # Replicate how data would be delivered in live

    for n in range(len(m5)):
        if n > 1:
            ndf = m5.iloc[:n + 1]

            # Trading for Asia range setup only between 7am and 12pm - Need to reset the variable at 1pm

            if (ndf.iloc[-1].time.hour >= 13):
                AH_grab = False
                Reaction_AH = False
                AH_Close_POI = False
                Take_Sell_AH = False
                Sell_AH_taken = False
                Time_AH_grab = 0
                Max_AH_time = 0

                AL_grab = False
                Reaction_AL = False
                AL_Close_POI = False
                Take_Buy_AL = False
                Buy_AL_taken = False
                Time_AL_grab = 0
                Max_AL_time = 0
                AR = []

            # Grab 96 previous 5min candle -> representing 8h so the Asian range
            # AR = [Asia high, low of AH POI, high of AL POI, Asia low]

            if ((ndf.iloc[-1].time.hour == 8) & (ndf.iloc[-1].time.minute == 0)):
                asia_session = ndf.iloc[-96:]
                AH = asia_session.high.max()
                AL = asia_session.low.min()
                AR += [asia_session.high.max()]
                AR += [asia_session[asia_session['high'] == AH].low.values[0]]
                AR += [asia_session[asia_session['low'] == AL].high.values[0]]
                AR += [asia_session.low.min()]

            # Need AR full to start investigating - collecting the time of the last candle on the datafram as it will be used later on
            if AR:
                candle_close_time = ndf.iloc[-1].time.to_pydatetime()

                # record AH grab when no trade possible
                if ((ndf.iloc[-1].high > AR[0]) & (AH_grab == False) & (Reaction_AH == False)):
                    AH_grab = True

                # record AL grab when no trade possible
                if ((ndf.iloc[-1].low < AR[3]) & (AL_grab == False) & (Reaction_AL == False)):
                    AL_grab = True

                    # record AH close POI
                if ((AH_grab == False) & (Reaction_AH == False) & (AH_Close_POI == False) &
                        (ndf.iloc[-1].iloc[2] > AR[1]) & (ndf.iloc[-1].iloc[2] <= AR[0])):
                    AH_Close_POI = True

                # record AL close POI
                if ((AL_grab == False) & (Reaction_AL == False) & (AL_Close_POI == False) &
                        (ndf.iloc[-1].iloc[3] >= AR[3]) & (ndf.iloc[-1].iloc[3] < AR[2])):
                    AL_Close_POI = True
                    # print(f'Close POI AL at {ndf.iloc[-1].time}')

                # record AH reaction
                if ((AH_grab == False) & (Reaction_AH == False) & (AH_Close_POI == True) &
                        (bear(ndf.iloc[-1]))):
                    Reaction_AH = True

                # record AL reaction
                if ((AL_grab == False) & (Reaction_AL == False) & (AL_Close_POI == True) &
                        (bull(ndf.iloc[-1]))):
                    Reaction_AL = True
                    # print(f'Reaction AL at {ndf.iloc[-1].time}')

                # record AH grab time to execute trade
                if ((AH_grab == False) & (Reaction_AH == True) & (ndf.iloc[-1].high > AR[0])):
                    AH_grab = True
                    Time_AH_grab = ndf.iloc[-1].time.to_pydatetime()
                    Max_AH_time = Time_AH_grab + timedelta(minutes=15)

                # record AL grab time to execute trade
                if ((AL_grab == False) & (Reaction_AL == True) & (ndf.iloc[-1].low < AR[3])):
                    AL_grab = True
                    Time_AL_grab = ndf.iloc[-1].time.to_pydatetime()
                    Max_AL_time = Time_AL_grab + timedelta(minutes=15)

                    # record Sell to trade
                # Only bear candle and within 15min needed to enter trade, still has speed and mostly bear to use (M1 tho)
                if ((AH_grab == True) & (Reaction_AH == True) & (bear(ndf.iloc[-1])) & (Sell_AH_taken == False)
                        & (speed(ndf, 8, 4, speed_factor))):
                    if candle_close_time <= Max_AH_time:
                        Take_Sell_AH = True
                        Sell_AH_taken = True
                        signal[n] = 1
                        sl[n] = last_high(ndf, 5) + buffer
                        dist_sl = abs(ndf.iloc[-1].close - sl[n])
                        tp[n] = ndf.iloc[-1].close - (rr * dist_sl)

                # record Buy to trade
                if ((AL_grab == True) & (Reaction_AL == True) & (bull(ndf.iloc[-1])) & (Buy_AL_taken == False)
                        & (speed(ndf, 8, 4, speed_factor))):
                    if candle_close_time <= Max_AL_time:
                        Take_Buy_AL = True
                        Buy_AL_taken = True
                        signal[n] = 2
                        sl[n] = last_low(ndf, 5) - buffer
                        dist_sl = abs(ndf.iloc[-1].close - sl[n])
                        tp[n] = ndf.iloc[-1].close + (rr * dist_sl)
                        # print(f'Buy trade {ndf.iloc[-1].time} ')

    m5.columns = ['Local time', 'Open', 'High', 'Low', 'Close', 'Volume', 'signal', '1']
    m5_backtest = m5.drop('1', axis=1)

    m5_backtest['signal'] = signal
    m5_backtest['sl'] = sl
    m5_backtest['tp'] = tp

    # function SIGNAL for backtesting

    df = m5_backtest[:]

    def SIGNAL():
        return df.signal

    # class AR_grab for backtesting

    class AR_grab(Strategy):
        percentage_per_trade = 0.01  # 1% risk per trade

        def init(self):
            super().init()
            self.signal1 = self.I(SIGNAL)

        def next(self):
            super().next()

            # code to sell

            if self.signal1 == 1:
                sl1 = self.data.sl[-1]
                tp1 = self.data.tp[-1]
                self.sell(sl=sl1, tp=tp1)

            # code to buy

            if self.signal1 == 2:
                sl1 = self.data.sl[-1]
                tp1 = self.data.tp[-1]
                self.buy(sl=sl1, tp=tp1)

    bt = Backtest(df, AR_grab, cash=100000, margin=1 / 500, commission=.00)
    stat = bt.run()
    bt.plot()
    expected_return = ((stat['Win Rate [%]'] / 100) * stat['# Trades'] * rr - (1 - (stat['Win Rate [%]'] / 100)) * stat[
        '# Trades'])

# 5th element of list is the backtesting.py table

    return [symbol, round(stat['Win Rate [%]'], 3), int(stat['# Trades']), expected_return, stat]
from LIT_trading_algo.functions import *
import MetaTrader5 as mt
from datetime import datetime, timedelta
import pandas as pd

# argument AR_list: list of 14 elements per pair

def asia_range_setup(AR_list, rr, buffer, speed_factor, risk):

    ndf = pd.DataFrame(mt.copy_rates_range(AR_list[0], mt.TIMEFRAME_M5, datetime.now() - timedelta(hours=1),
                                           datetime.now() + timedelta(hours=3)))
    ndf['time'] = pd.to_datetime(ndf['time'], unit='s')

    # Need AR full to start investigating
    if AR_list[1]:
        candle_close_time = ndf.iloc[-2].time.to_pydatetime()

        # record AH grab when no trade possible
        if ((ndf.iloc[-2].high > AR_list[1][0]) & (AR_list[2] == False) & (AR_list[3] == False)):
            AR_list[2] = True
            print(f'AH grab and no trade at {ndf.iloc[-1].time} for {AR_list[0]} with last high: {ndf.iloc[-2].high} and AH: {AR_list[1][0]}')

        # record AL grab when no trade possible
        if ((ndf.iloc[-2].low < AR_list[1][3]) & (AR_list[8] == False) & (AR_list[9] == False)):
            AR_list[8] = True
            print(f'AL grab and no trade at {ndf.iloc[-1].time} for {AR_list[0]} with last low: {ndf.iloc[-2].low} and AL: {AR_list[1][3]}')

        # record AH close POI
        if ((AR_list[2] == False) & (AR_list[3] == False) & (AR_list[4] == False) &
                (ndf.iloc[-2].high > AR_list[1][1]) & (ndf.iloc[-2].high <= AR_list[1][0])):
            AR_list[4] = True
            print(f'Close POI AH at {ndf.iloc[-2].time} for {AR_list[0]} with candle close high: {ndf.iloc[-2].high} in between {AR_list[1][0]} and {AR_list[1][1]}')

        # record AL close POI
        if ((AR_list[8] == False) & (AR_list[9] == False) & (AR_list[10] == False) &
                (ndf.iloc[-2].low >= AR_list[1][3]) & (ndf.iloc[-2].low < AR_list[1][2])):
            AR_list[10] = True
            print(f'Close POI AL at {ndf.iloc[-2].time} for {AR_list[0]} with candle close low: {ndf.iloc[-2].low} in between {AR_list[1][2]} and {AR_list[1][3]}')

        # record AH reaction
        if ((AR_list[2] == False) & (AR_list[3] == False) & (AR_list[4] == True) &
                (bear(ndf.iloc[-2]))):
            AR_list[3] = True
            print(f'Reaction AH at {ndf.iloc[-2].time} for {AR_list[0]} with candle close high: {ndf.iloc[-2].high} in between {AR_list[1][0]} and {AR_list[1][1]}')

        # record AL reaction
        if ((AR_list[8] == False) & (AR_list[9] == False) & (AR_list[10] == True) &
                (bull(ndf.iloc[-2]))):
            AR_list[9] = True
            print(f'Reaction AL at {ndf.iloc[-2].time} for {AR_list[0]} with candle close low: {ndf.iloc[-2].low} in between {AR_list[1][2]} and {AR_list[1][3]}')

        # record AH grab time to execute trade
        if ((AR_list[2] == False) & (AR_list[3] == True) & (ndf.iloc[-2].high > AR_list[1][0])):
            AR_list[2] = True
            AR_list[6] = ndf.iloc[-2].time.to_pydatetime()
            AR_list[7] = AR_list[6] + timedelta(minutes=15)
            print(f'AH grab and trade possible at {ndf.iloc[-2].time} for {AR_list[0]} with candle close high: {ndf.iloc[-2].high}')

        # record AL grab time to execute trade
        if ((AR_list[8] == False) & (AR_list[9] == True) & (ndf.iloc[-1].low < AR_list[1][3])):
            AR_list[8] = True
            AR_list[12] = ndf.iloc[-2].time.to_pydatetime()
            AR_list[13] = AR_list[12] + timedelta(minutes=15)
            print(f'AL grab and trade possible at {ndf.iloc[-2].time} for {AR_list[0]} with candle close low: {ndf.iloc[-2].low}')

        # record Sell to trade
        # Only bear candle and within 15min needed to enter trade, still has speed and mostly bear to use (M1 tho)
        if ((AR_list[2] == True) & (AR_list[3] == True) & (bear(ndf.iloc[-2])) & (AR_list[5] == False) & (
        speed(ndf, 8, 4, speed_factor))):
            if candle_close_time <= AR_list[7]:
                AR_list[5] = True
                sell = mt.ORDER_TYPE_SELL

                sell_price = mt.symbol_info_tick(AR_list[0]).bid
                sl = last_high(ndf, 5) + buffer
                dist_sl = abs(ndf.iloc[-2].close - sl)
                lot = calculate_lot(AR_list[0], mt.account_info().balance, risk, dist_sl, sell_price)
                tp = ndf.iloc[-2].close - (rr * dist_sl)
                open_position(AR_list[0], lot, sell, sell_price, sl, tp)

                print(f'Sell trade {ndf.iloc[-1].time} for {AR_list[0]} with entry: {sell_price}, sl: {sl} and tp: {tp}')

        # record Buy to trade
        if ((AR_list[8] == True) & (AR_list[9] == True) & (bull(ndf.iloc[-2])) & (AR_list[11] == False) & (
        speed(ndf, 8, 4, speed_factor))):
            if candle_close_time <= AR_list[13]:
                AR_list[11] = True
                buy = mt.ORDER_TYPE_BUY
                buy_price = mt.symbol_info_tick(AR_list[0]).ask
                sl = last_low(ndf, 5) - buffer
                dist_sl = abs(ndf.iloc[-2].close - sl)
                lot = calculate_lot(AR_list[0], mt.account_info().balance, risk, dist_sl, buy_price)
                tp = ndf.iloc[-2].close + (rr * dist_sl)
                open_position(AR_list[0], lot, buy, buy_price, sl, tp)
                print(f'Buy trade {ndf.iloc[-1].time} for {AR_list[0]} with entry: {buy_price}, sl: {sl} and tp: {tp}')

    return AR_list
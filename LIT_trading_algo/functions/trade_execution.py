import MetaTrader5 as mt

def open_position(symbol, lot, order_type, price, sl, tp):     # works great
    request = {
        "action": mt.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": sl,  #float
        "tp": tp,  #float
        "comment": "python script open",
        "type_time": mt.ORDER_TIME_GTC,
        "type_filling": mt.ORDER_FILLING_IOC,
}
    order = mt.order_send(request)
    return order

def close_position(symbol, lot, order_type, position_num, price):   # works, don't forget to put opposite order type to close
    request = {
        "action": mt.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        'position': position_num,
        "price": price,
        "comment": "Close position",
        "type_time": mt.ORDER_TIME_GTC,
        "type_filling": mt.ORDER_FILLING_IOC,
}
    order = mt.order_send(request)
    return order


# pips_sl corresponds to the price difference between current price and stop loss level
# function working
def calculate_lot(symbol, balance, risk, pips_sl, current_price):
    if 'JPY' in symbol:
        pip_value = ((0.01 / current_price) * 100000) * 100
    else:
        pip_value = ((0.0001 / current_price) * 100000) * 10000

    lot = (balance * risk) / ((pips_sl) * pip_value)

    return round(lot, 2)

import websocket
import json
import numpy as np
import talib
from binance.client import Client
from binance.enums import *
import config
import streamlit as st
import threading
import pandas as pd
ws=None
socket = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

closes = []
client = Client(config.API_KEY, config.SECRET_KEY, testnet=True)
in_position = False
initial_cash = 10000
current_cash = 10000
rsi_period = 14
rsi_overbought = 70
rsi_oversold = 30
trade_quantity = 0.05
trade_symbol = "ETHUSDT"


rsi_placeholder = st.empty()
cur_money = st.empty()
action_placeholder = st.empty()

def calculating_total_profit(side, amount):
    global initial_cash, current_cash
    if side == SIDE_SELL:
        profit_loss = current_cash + amount - initial_cash
        current_cash += amount
        action_placeholder.write(f"Profit/Loss from trade: {profit_loss}")
    else:
        current_cash -= amount
        cur_money.write(f"Current Cash: {current_cash}")

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("Sending order...")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        fill = order['fills']
        for item in fill:
            price = float(item['price'])
            qty = float(item['qty'])
            amount = price * qty
            calculating_total_profit(side, amount)
    except Exception as e:
        action_placeholder.write(f"An exception occurred: {e}")
        return False
    return True

def fetch_historic_data(symbol, interval, lookback):
    candles = client.get_historical_klines(symbol, interval, lookback)
    historical_closes = [float(candle[4]) for candle in candles]  
    return historical_closes




short_period=9
long_period=200
live_data = pd.DataFrame(columns=['timestamp', 'close'])

last_signal = None  
def stop():
    ws.close()
    c="live trading stopped"

    return c 

def moving_average(ws, message):
    global live_data, last_signal
    data = json.loads(message)
    print("recieved")
    timestamp = pd.to_datetime(data['E'], unit='ms')  
    close_price = float(data['k']['c'])  

    new_row = {'timestamp': timestamp, 'close': close_price}
    live_data = pd.concat([live_data, pd.DataFrame([new_row])], ignore_index=True)

    live_data = live_data.iloc[-500:]

    if len(live_data) >= long_period:
        live_data['SMA_Short'] = talib.SMA(live_data['close'], timeperiod=short_period)
        live_data['SMA_Long'] = talib.SMA(live_data['close'], timeperiod=long_period)

        last_row = live_data.iloc[-1]
        prev_row = live_data.iloc[-2] if len(live_data) > 1 else None

        if prev_row is not None:
            if (prev_row['SMA_Short'] <= prev_row['SMA_Long']) and (last_row['SMA_Short'] > last_row['SMA_Long']):
                if last_signal != "BUY":
                    #order_succeeded =True# order(SIDE_BUY, trade_quantity, trade_symbol)
                    #if order_succeeded:
                        
                    print(f"BUY Signal at {last_row['timestamp']} - Price: {last_row['close']}")
                    action_placeholder.write(f"BUY Signal at {last_row['timestamp']} - Price: {last_row['close']}")
                    last_signal = "BUY"

            elif (prev_row['SMA_Short'] >= prev_row['SMA_Long']) and (last_row['SMA_Short'] < last_row['SMA_Long']):
                if last_signal != "SELL":
                    #order_succeeded =True# order(SIDE_SELL, trade_quantity, trade_symbol)
                    #if order_succeeded:
                        
                    print(f"SELL Signal at {last_row['timestamp']} - Price: {last_row['close']}")
                    action_placeholder.write(f"SELL Signal at {last_row['timestamp']} - Price: {last_row['close']}")
                    last_signal = "SELL"






def on_rsi(ws, message):
    global closes, in_position
    message = json.loads(message)
    print("recieved")
    if "k" in message and message["k"]["x"]:  
        close = message['k']['c']  
        closes.append(float(close))  

        if len(closes) > rsi_period:
            np_closes = np.array(closes)
            rsi = talib.RSI(np_closes, rsi_period)
            last_rsi = rsi[-1]
            
            rsi_placeholder.write(f"Current RSI: {last_rsi}")

            if last_rsi > rsi_overbought:
                if in_position:
                    action_placeholder.write("Sell!! Sell!!")
                    order_succeeded =True# order(SIDE_SELL, trade_quantity, trade_symbol)
                    if order_succeeded:
                        in_position = False
                else:
                    action_placeholder.write("A sell signal , but you don't own any.")
            elif last_rsi < rsi_oversold:
                if in_position:
                    action_placeholder.write("A buy signal but You already own it!")
                else:
                    action_placeholder.write("Buy! Buy!")
                    order_succeeded =True# order(SIDE_BUY, trade_quantity, trade_symbol)
                    if order_succeeded:
                        in_position = True

       

def initialize_live_data(symbol, interval, lookback):
    global live_data
    candles = client.get_historical_klines(symbol, interval, lookback)
    data = {
        "timestamp": [pd.to_datetime(candle[0], unit="ms") for candle in candles],
        "close": [float(candle[4]) for candle in candles],
    }
    live_data = pd.DataFrame(data)

def real_call(on_message, money, rsi_o, rsi_s, rsi_p, tr_q, sym,pla,plaa,lookback):
    global initial_cash, current_cash, rsi_overbought, rsi_oversold, rsi_period, trade_quantity, trade_symbol,rsi_placeholder,action_placeholder,live_data
    initial_cash = money
    current_cash = money
    rsi_placeholder=pla
    action_placeholder=plaa
    trade_symbol = sym

    if on_message=="Moving":
        initialize_live_data(trade_symbol,Client.KLINE_INTERVAL_1MINUTE, f"{long_period} minutes ago UTC")


    else:

        rsi_overbought = rsi_o
        rsi_oversold = rsi_s
        rsi_period = rsi_p
        trade_quantity = tr_q
        
        



        historical_closes = fetch_historic_data(trade_symbol, Client.KLINE_INTERVAL_1MINUTE, f"{rsi_period} minutes ago UTC")
        closes.extend(historical_closes)  
    global ws
    ws = websocket.WebSocketApp(socket ,on_message = on_message)
    ws.run_forever()



import websocket
import json,talib
import numpy as np
from binance.client import Client
from binance.enums import *
import config
import streamlit as st



socket ="wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
closes=[]
client = Client(config.API_KEY,config.SECRET_KEY,testnet=True)
in_position=False
initial_cash=10000
current_cash=10000
rsi_period=14
rsi_overbrought=70
rsi_oversold=30
trade_quantity=0.05
trade_symbol="ETHUSDT"

with st.sidebar:

    rsi_placeholder=st.empty()
    cur_money=st.empty()
# Create a placeholder for displaying trading actions
action_placeholder = st.empty()

def calculating_total_profit(side,amount):
    global initial_cash,current_cash
    if side==SIDE_SELL:
        profit_loss=current_cash+amount - initial_cash
        current_cash+=amount
        action_placeholder.write(f"Profit/Loss from trade: {profit_loss}")
    else: 
        current_cash-=amount
        cur_money.write(current_cash)


    
        


def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        fill =order['fills']
        for item in fill:
            price = float(item['price'])
            qty = float(item['qty'])
            amount=price*qty
            calculating_total_profit(side,amount)

        
    except Exception as e:
        action_placeholder.write(f"An exception occurred: {e}")
        return False

    return True
def fetch_historic_data(symbol, interval, lookback):
    # Fetch the last 'lookback' candles to get the historical closing prices
    candles = client.get_historical_klines(symbol, interval, lookback)
    historical_closes = [float(candle[4]) for candle in candles]  # Close prices are in the 5th column
    return historical_closes





def on_rsi(ws,message):
    
    print("recieved")
    global closes,in_position
    message = json.loads(message)
    close = message['k']['c']
    is_closed = message['k']['x']
    if is_closed:
        closes.append(float(close))
        print("closes")
        print(closes)
        if len(closes)>rsi_period:
            np_closes = np.array(closes)
            rsi = talib.RSI(np_closes,rsi_period)
            print(rsi[-1])
            last = rsi[-1]
            
            rsi_placeholder.write(f"Current RSI: {last}")
            if last > rsi_overbrought:
                if in_position:
                    action_placeholder.write("Sell!! Sell!!")
                    order_succeeded = order(SIDE_SELL, trade_quantity, trade_symbol)
                    if order_succeeded:
                        in_position = False
                else:
                    action_placeholder.write("you could sell at the price but you dont own any")
            if last < rsi_oversold:
                if in_position:
                     action_placeholder.write("you already bought it so you already hv it")
                else:
                     action_placeholder.write("buy! buy!")
                     order_succeeded = order(SIDE_BUY, trade_quantity, trade_symbol)
                     if order_succeeded:
                        in_position = True
def real_call(on_message,money,rsi_o,rsi_s,rsi_p,tr_q,sym):
    global initial_cash,current_cash,rsi_overbrought,rsi_oversold,rsi_period,trade_quantity,trade_symbol
    initial_cash=money
    current_cash=money
    rsi_overbrought=rsi_o
    rsi_oversold=rsi_s
    rsi_period=rsi_p
    trade_quantity=tr_q
    trade_symbol=sym
    historical_closes = fetch_historic_data("ETHUSDT", Client.KLINE_INTERVAL_1MINUTE, f"{rsi_period} minutes ago UTC")
    closes.extend(historical_closes)
    ws = websocket.WebSocketApp(socket ,on_message = on_message)
    ws.run_forever()

  # Add the historical closes to the closes list

# Start WebSocket



# Show a message while waiting for real-time data


# Keep Streamlit app running


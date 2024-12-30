import websocket
import json,talib
import numpy as np
from binance.client import Client
from binance.enums import *
import config
import pandas as pd
import streamlit as st
#from real_data import *
from real_data import *
from strategy import *
from main import *


socket ="wss://stream.binance.com:9443/ws/ethusdt@kline_1m"



def you(client):
     
    info = client.get_account()
    balance = info['balances']
    available =[]
    asset=[]
    
    for dict in balance:
        free = dict["free"]
        name=dict["asset"]
        if name =="USDT":
            money =free
        available.append(free)
        asset.append(name)
    df=pd.DataFrame({
        "available":available,
        "name":asset
    })
    return df,float(money)

def main():
     st.title("Your Account")
     client = Client(config.API_KEY,config.SECRET_KEY,testnet=True)

     df,money=you(client)
     st.write(df)
     st.write(f"Initial USDT you have to make buys:{money}")
     symbol= st.text_input("Enter the symbol name")
     activity = st.selectbox("Choose",("live trading","backtest"))
     pla=st.sidebar.empty()
     plaa=st.sidebar.empty()
     if activity=="backtest":
        strategy_choice = st.selectbox("Choose Strategy", ("Mean Reversion", "Moving Average Crossover", "Momentum Strategy"))

        if strategy_choice == "Mean Reversion":
            strategy_class = MeanReversion
            bollinger_period = st.number_input("Bollinger Period", value=20)
            bollinger_dev = st.number_input("Bollinger Dev", value=2)
            rsi_period = st.number_input("RSI Period", value=14)
            rsi_oversold = st.number_input("RSI Oversold", value=30)
            rsi_overbought = st.number_input("RSI Overbought", value=70)
            strategy_params = {
            'bollinger_period': bollinger_period,
            'bollinger_dev': bollinger_dev,
            'rsi_period': rsi_period,
            'rsi_oversold': rsi_oversold,
            'rsi_overbought': rsi_overbought
        }

        elif strategy_choice == "Moving Average Crossover":
            strategy_class = MovingAverageCrossover
            short_period = st.number_input("Short SMA Period", value=20)
            long_period = st.number_input("Long SMA Period", value=50)
            rsi_period = st.number_input("RSI Period", value=14)
            rsi_overbought = st.number_input("RSI Overbought", value=70)
            rsi_oversold = st.number_input("RSI Oversold", value=30)
            
            strategy_params = {
            'short_period': short_period,
            'long_period': long_period,
            'rsi_period': rsi_period,
            'rsi_overbought': rsi_overbought,
            'rsi_oversold': rsi_oversold
        }
      

        elif strategy_choice == "Momentum Strategy":
            strategy_class = MomentumStrategy
            momentum_period = st.number_input("Momentum Period", value=100)
            roc_threshold = st.number_input("ROC Threshold", value=0)
        
            strategy_params = {
            'momentum_period': momentum_period,
            'roc_threshold': roc_threshold
        }

        if st.button("Run Backtest"):
            st.write("Running portfolio backtest... Please wait.")
            cerebro = run_backtest(strategy_class,strategy_params,symbol,money)
            cerebro.plot()
     else:
        live_strategy=st.selectbox("choose:",("RSI","MOVING AVERAGE"))
        if live_strategy=="RSI":

            rsi_p=st.number_input("Enter RSI period Value",value=14)
            rsi_ob=st.number_input("Enter rsi overbought",value =70)
            rsi_os=st.number_input("Enter rsi overbought",value =30)
            trade_q=st.number_input("Eenter trade quantity",value =0.05)

            if st.button("start live trading"):

                real_call(on_rsi,money,rsi_ob,rsi_os,rsi_p,trade_q,symbol,pla,plaa,rsi_p)      
            if st.button("stop live trading"):
                c=stop()
                st.write(c)   
        else:
            #period =st.number_input("Enter from which time u want to start",value=30)
            trade_q=st.number_input("Eenter trade quantity",value =0.05)


            if st.button("start live trading"):

                real_call(moving_average,money,70,30,14,trade_q,symbol,pla,plaa,0) 
            if st.button("stop live trading"):
                c=stop()
                st.write(c)     
        

     
     
    

if __name__ == "__main__":
    main()

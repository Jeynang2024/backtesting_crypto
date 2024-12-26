import websocket
import json,talib
import numpy as np
from binance.client import Client
from binance.enums import *
import config
import pandas as pd
import streamlit as st
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
     if activity=="backtest":
        strategy_choice = st.selectbox("Choose Strategy", ("Mean Reversion", "Moving Average Crossover", "Momentum Strategy"))

        if strategy_choice == "Mean Reversion":
            strategy_class = MeanReversion
        elif strategy_choice == "Moving Average Crossover":
            strategy_class = MovingAverageCrossover
        elif strategy_choice == "Momentum Strategy":
            strategy_class = MomentumStrategy

        if st.button("Run Backtest"):
            st.write("Running portfolio backtest... Please wait.")
            cerebro = run_backtest(strategy_class,symbol,money)
            cerebro.plot()
     else:
        rsi_p=st.number_input("Enter RSI period Value",value=14)
        rsi_ob=st.number_input("Enter rsi overbought",value =70)
        rsi_os=st.number_input("Enter rsi overbought",value =30)
        trade_q=st.number_input("Eenter trade quantity",value =0.05)
        if st.button("start live trading"):

            real_call(on_rsi,money,rsi_ob,rsi_os,rsi_p,trade_q,symbol)      
        

     
     
    

# This is how Streamlit expects the main function to be run
if __name__ == "__main__":
    main()
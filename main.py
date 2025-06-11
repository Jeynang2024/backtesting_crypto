import streamlit as st
import backtrader as bt
import numpy as np
from strategy import *
import pandas as pd
from his_data import *
from binance.client import Client
import config



client = Client(config.API_KEY,config.SECRET_KEY)



def run_backtest(strategy_class,strategy_params,symbol,initial_cash,start,end,interval):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(strategy_class,**strategy_params)
    data = fetch_historical_data(symbol,client,start,end,interval)
    data_feed =bt.feeds.GenericCSVData(
        dataname=data,
            datetime=0,
            open=1,
            high=2,
            low=3,
            close=4,
            volume=5,
            openinterest=-1,
            dtformat=('%Y-%m-%d %H:%M:%S') 
    )
    cerebro.adddata(data_feed,name=symbol)
    cerebro.broker.set_cash(initial_cash)
    strategies = cerebro.run()
    
    # Access the first strategy instance
    strategy_instance = strategies[0]
    
    # Access buy_signals and sell_signals
    buy_signals = strategy_instance.buy_signals
    sell_signals = strategy_instance.sell_signals
    columns_to_read = ['Open time',  'Close']
    datas=pd.read_csv(data, usecols=columns_to_read)
    #print(datas)
    # Print the buy_signals
    #print("Buy Signals:", buy_signals)
    

# Now you can access buy_signals
    #print(buy_signals)


    return cerebro ,datas, buy_signals,sell_signals


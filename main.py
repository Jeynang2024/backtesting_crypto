import streamlit as st
import backtrader as bt
import numpy as np
from strategy import *
import pandas as pd
from his_data import *
from binance.client import Client
import config



client = Client(config.API_KEY,config.SECRET_KEY)



def run_backtest(strategy_class,symbol,initial_cash):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(strategy_class)
    data = fetch_historical_data(symbol,client)
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
    cerebro.run()
    return cerebro


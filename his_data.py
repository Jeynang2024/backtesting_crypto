from binance.client import Client
import pandas as pd
import config

client = Client(config.API_KEY,config.SECRET_KEY)
def fetch_historical_data(symbol,client):
    klines_data =client.get_historical_klines(symbol,'1h','30 days ago UTC')
    df = pd.DataFrame(klines_data,columns=[
        'Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 
    'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 
    'Taker buy quote asset volume', 'Ignore'
    ])
    df = df[['Open time', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df["Open time"]=pd.to_datetime(df['Open time'],unit="ms")
    df.set_index('Open time', inplace=True)
    df.to_csv(f'{symbol}.csv', index=True)
    data =f"{symbol}.csv"

    return data



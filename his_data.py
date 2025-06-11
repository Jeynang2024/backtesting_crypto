from binance.client import Client
import pandas as pd
import config

client = Client(config.API_KEY,config.SECRET_KEY)
def fetch_historical_data(symbol,client,start,end,interval):
    ''' klines_data =client.get_historical_klines(symbol,'1h','30 days ago UTC')'''
    print("fetching")
    start_str = start.strftime('%Y-%m-%d %H:%M:%S')  # e.g., '2023-01-01 00:00:00'
    end_str = end.strftime('%Y-%m-%d %H:%M:%S')      # e.g., '2023-01-15 00:00:00'
    
    # Fetch historical klines (candlestick data)
    klines_data = client.get_historical_klines(symbol, interval, start_str, end_str)

    # Convert the kline data into a Pandas DataFrame for easier analysis

    # Convert timestamp to datetime
    df = pd.DataFrame(klines_data,columns=[
        'Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 
    'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 
    'Taker buy quote asset volume', 'Ignore'
    ])
    df = df[['Open time', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df["Open time"]=pd.to_datetime(df['Open time'],unit="ms")
    df['Open time'] = df['Open time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df.set_index('Open time', inplace=True)
    df.to_csv(f'{symbol}.csv', index=True)
    data =f"{symbol}.csv"

    return data



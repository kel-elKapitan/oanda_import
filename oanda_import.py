# load standard packages

import pandas as pd
import requests
from datetime import timezone, datetime

# Load OANDA packages

import oandapyV20
import oandapyV20.endpoints.instruments as instruments

# set a startdate and a timeframe

start_datetime = datetime(1990, 1, 1)
timeframe = "D"
my_access_token = "c49461616d83b16e43fe7d192b6ccb07-cbb08973f2faa3f32ccc2bfa74103a58"

# function to find the latest or most up to date timestamp

def OANDA_Connection_Latest(pair):
    global timeframe

    client = oandapyV20.API(access_token=my_access_token)

    params = {"count": 1, "granularity": timeframe}

    r = instruments.InstrumentsCandles(instrument=pair, params=params)

    client.request(r)
    r.response['candles'][0]['mid']
    r.response['candles'][0]['time']
    r.response['candles'][0]['volume']
    dat = []
    
    for oo in r.response['candles']:
        dat.append([oo['time']])
        df = pd.DataFrame(dat)
        df.columns = ['Time']
        
    #Convert To Float
    df["Time"] = pd.to_datetime(df["Time"], unit='ns')
    latest_datetime = int((df['Time'].iloc[0]).replace(tzinfo=timezone.utc).timestamp())
    
    return latest_datetime


# function to download 5000 entries at a time

def OANDA_Connection(active_datetime, pair):
    global timeframe
    client = oandapyV20.API(access_token=my_access_token)
    params = {"from": active_datetime, "count": 5000, "granularity": timeframe}
    
    r = instruments.InstrumentsCandles(instrument=pair, params=params)
    
    client.request(r)
    
    r.response['candles'][0]['mid']
    r.response['candles'][0]['time']
    r.response['candles'][0]['volume']
    
    dat = []
    
    for oo in r.response['candles']:
        dat.append([oo['time'], oo['mid']['o'], oo['mid']['h'], oo['mid']['l'], oo['mid']['c'], oo['volume'], oo['complete']])
        df = pd.DataFrame(dat)
        df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Complete']
        
    #Convert To Float
    df["Time"] = pd.to_datetime(df["Time"], unit='ns')
    df["Open"] = pd.to_numeric(df["Open"], downcast="float")
    df["High"] = pd.to_numeric(df["High"], downcast="float")
    df["Low"] = pd.to_numeric(df["Low"], downcast="float")
    df["Close"] = pd.to_numeric(df["Close"], downcast="float")
    
    return df



def DownloadData(pair):
    global start_datetime
    start_unix = int(start_datetime.replace(tzinfo=timezone.utc).timestamp())
    latest_datetime = OANDA_Connection_Latest(pair)
    active_datetime = start_unix
    all_data = pd.DataFrame([])
    
    while active_datetime != latest_datetime:
        df = OANDA_Connection(active_datetime, pair)
        last_row = df.tail(1)

        active_datetime = int((last_row['Time'].iloc[0]).replace(tzinfo=timezone.utc).timestamp())
    all_data = all_data.append(df)
    all_data = all_data.reset_index()
    all_data = all_data.drop(['index'], axis=1)

    return all_data


def DownloadAllPairs():
    #Download All Currency Pairs
    
    pairs = ['EUR_USD', 'AUD_USD', 'GBP_USD', 'NZD_USD', 'USD_CAD', 'USD_CHF', 'USD_JPY']
    
    for pair in pairs:
        pair_data = DownloadData(pair)
        print(pair + " Downloaded\n\n")
        pair_data.to_csv('Data_' + pair + '.csv', index=False)
        print((pair + " Saved to csv file: DATA_" + pair + ".csv"))
    return


DownloadAllPairs()
print("7 instruments downloaded from " + str(start_datetime) + " to the latest candle")
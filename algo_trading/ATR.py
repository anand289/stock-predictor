#ATR: Average True Range --> For volatility
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 19:57:17 2023

@author: anandsingh
"""

import numpy as np
import yfinance as yf
import datetime

# List of stocks we need the data for
tickers = ['TSLA','AAPL','SPY']
ohlcv_data = {}

# creating a dictionary where key is the ticker name and value is the dataframe with ohlcv_data
for ticker in tickers:
    temp = yf.download(ticker,period='1mo',interval='15m')
    temp.dropna(how='any',inplace=True)
    ohlcv_data[ticker] = temp
    
def ATR(DF,n =14):
    df = DF.copy()
    df['H-L'] = df['High'] - df['Low']
    df['H-PC'] = df['High'] - df['Adj Close'].shift(1)
    df['L-PC'] = df['Low'] - df['Adj Close'].shift(1)
    df['TR'] = df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].ewm(span=n, min_periods=n).mean()
    return df['ATR']

for ticker in ohlcv_data:
    ohlcv_data[ticker]['ATR'] = ATR(ohlcv_data[ticker])
    


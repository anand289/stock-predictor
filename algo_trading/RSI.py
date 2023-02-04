#RSI-> Relative Strength Indicator --> Momentum Indicator
#>70 overbought correction in expeced --> expected to go down
#<30 asset in oversold --> expected to go up
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 23:41:48 2023

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
    temp = yf.download(ticker,period='1mo',interval='5m')
    temp.dropna(how='any',inplace=True)
    ohlcv_data[ticker] = temp


def RSI(DF,n=14):
    df = DF.copy()
    df['change'] = df['Adj Close'] - df['Adj Close'].shift(1)
    df['gain'] = np.where(df['change']>=0,df['change'],0)
    df['loss'] = np.where(df['change']<0,-1*df['change'],0)
    df['avgGain'] = df['gain'].ewm(alpha=1/n,min_periods=n).mean()
    df['avgLoss'] = df['loss'].ewm(alpha=1/n,min_periods=n).mean()
    df['rs'] = df['avgGain']/df['avgLoss']
    df['rsi'] = 100 - (100/(1+df['rs']))
    return df['rsi']

for ticker in ohlcv_data:
    ohlcv_data[ticker]["RSI"] = RSI(ohlcv_data[ticker])
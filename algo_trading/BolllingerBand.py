# Volitality indicator
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
    temp = yf.download(ticker,period='1mo',interval='5m')
    temp.dropna(how='any',inplace=True)
    ohlcv_data[ticker] = temp
    
def Boll_Band(DF,n=14):
    df = DF.copy()
    df['MB'] = df['Adj Close'].rolling(n).mean()
    df['UB'] = df['MB'] + 2*df['Adj Close'].rolling(n).std(ddof=0)
    df['LB'] = df['MB'] - 2*df['Adj Close'].rolling(n).std(ddof=0)
    df['BB_Width'] = df['UB'] - df['LB']
    return df[['MB','UB','LB','BB_Width']]

for ticker in tickers:
    ohlcv_data[ticker][['MB','UB','LB','BB_Width']] = Boll_Band(ohlcv_data[ticker],20)
    
#Moving Average Convergence Divergence
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 15:34:18 2023

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

# funcition to calculate and return MACD and SIGNAL coloums
def MACD(DF,a=12,b=26,c=9):
    df = DF.copy()
    df['ma_fast'] = df["Adj Close"].ewm(span=a,min_periods=a).mean()
    df['ma_slow'] = df["Adj Close"].ewm(span=b,min_periods=b).mean()
    df['macd'] =df['ma_fast'] - df['ma_slow']
    df['signal'] = df['macd'].ewm(span=c,min_periods=c).mean()
    return df.loc[:,['macd','signal']]

# adding MACD and SIGNAL to ohlcv_data
for ticker in ohlcv_data:
    ohlcv_data[ticker][['MACD','SIGNAL']] = MACD(ohlcv_data[ticker])
    
    
    
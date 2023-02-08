#CAGR ---> Compounded Annual Growth Rate
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 22:45:02 2023

@author: anandsingh
"""

import numpy as np
import yfinance as yf
import datetime

# List of stocks we need the data for
tickers = ['TSLA']
ohlcv_data = {}

# Creating a dictionary where key is the ticker name and value is the dataframe with ohlcv_data
for ticker in tickers:
    temp = yf.download(ticker,period='5y',interval='1d')
    temp.dropna(how='any',inplace=True)
    ohlcv_data[ticker] = temp
  
def CAGR(DF):
    df = DF.copy()
    df['return'] = df['Adj Close'].pct_change()
    df['cum_return'] = (1+df['return']).cumprod()
    n = len(df)/252 # this formula will only work if your interval is in days.
    CAGR = (df['cum_return'][-1])**(1/n)-1
    return CAGR

for ticker in ohlcv_data:
    print('CAGR for {} = {}'.format(ticker,CAGR(ohlcv_data[ticker])))
    

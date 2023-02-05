# Annualized Volitality
# Widely used metric for risk
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 00:20:54 2023

@author: anandsingh
"""

import numpy as np
import yfinance as yf
import datetime

# List of stocks we need the data for
tickers = ['TSLA','ASML','SPY']
ohlcv_data = {}

# Creating a dictionary where key is the ticker name and value is the dataframe with ohlcv_data
for ticker in tickers:
    temp = yf.download(ticker,period='10y',interval='1d')
    temp.dropna(how='any',inplace=True)
    ohlcv_data[ticker] = temp
    
def volatility(DF):
    df = DF.copy()
    df['return'] = df['Adj Close'].pct_change()
    vol = df['return'].std()*np.sqrt(252)
    return vol

for ticker in ohlcv_data:
    print("Volatility of {} = {}".format(ticker,volatility(ohlcv_data[ticker])))
#ADX--> Average Directional Index. Strength of the trend
#0-25 -- no trend
#25-50 -- Strong trend
#50-75 -- Very strong trend
#75-100 -- Extremely strong trend
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 00:11:40 2023

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
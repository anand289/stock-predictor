#Sharpe Ratio: Average return earned in excess of the risk free 
# rate per unit of volatility. 
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 00:28:28 2023

@author: anandsingh
"""

import numpy as np
import yfinance as yf
import datetime

# List of stocks we need the data for
tickers = ['SPY']
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

def volatility(DF):
    df = DF.copy()
    df['return'] = df['Adj Close'].pct_change()
    vol = df['return'].std()*np.sqrt(252)
    return vol

def sharpe(DF,rf): # rf -> risk free rate. 3% is the last 30 year risk free return of US government bonds. Can find it on Google  
    df = DF.copy()
    return (CAGR(df)-rf)/volatility(df) 


for ticker in ohlcv_data:
    print("Sharpe-ratio of {} = {}".format(ticker,sharpe(ohlcv_data[ticker],0.025)))


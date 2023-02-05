#MAximum Drawdown-> Largest percentage drop in asset price over a specified time period.
# very important risk parameter

# Calmar Ratio-> CAGR/Maximum Drawdown
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 00:43:39 2023

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
 
def CAGR(DF):
    df = DF.copy()
    df['return'] = df['Adj Close'].pct_change()
    df['cum_return'] = (1+df['return']).cumprod()
    n = len(df)/252 # this formula will only work if your interval is in days.
    CAGR = (df['cum_return'][-1])**(1/n)-1
    return CAGR    
 
def max_dd(DF):
    df = DF.copy()
    df['return'] = df['Adj Close'].pct_change()
    df['cum_return'] = (1+df['return']).cumprod()
    df['cum_roll_max'] = df['cum_return'].cummax()
    df['drawdown'] = df['cum_roll_max'] - df['cum_return']
    return (df['drawdown']/df['cum_roll_max']).max()

def calmar(DF):
    df = DF.copy()
    return CAGR(df)/max_dd(DF)
    
for ticker in ohlcv_data:
    print("max drawdown of {} = {}".format(ticker,max_dd(ohlcv_data[ticker])))
    print("calmar-ratio of {} = {}".format(ticker,calmar(ohlcv_data[ticker])))
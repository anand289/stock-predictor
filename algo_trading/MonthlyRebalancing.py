#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 09:51:51 2023

@author: anandsingh

Run this script at the 1st (not on 31st because script will not replace 
                            bad performing stocks until the month end)
                            of every month and buy $500 of "Current Portfolio"
"""

import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import copy
import matplotlib.pyplot as plt

#%% KPIs

def CAGR(DF):
    df = DF.copy()
    df['cum_return'] = (1+df['mon_return']).cumprod()
    n = len(df)/12 
    CAGR = (df['cum_return'].tolist()[-1])**(1/n)-1
    return CAGR

def volatility(DF):
    df = DF.copy()
    vol = df['mon_return'].std()*np.sqrt(12)
    return vol

def sharpe(DF,rf): # rf -> risk free rate. 3% is the last 30 year risk free return of US government bonds. Can find it on Google  
    df = DF.copy()
    return (CAGR(df)-rf)/volatility(df) 

def max_dd(DF):
    df = DF.copy()
    df['cum_return'] = (1+df['mon_return']).cumprod()
    df['cum_roll_max'] = df['cum_return'].cummax()
    df['drawdown'] = df['cum_roll_max'] - df['cum_return']
    return (df['drawdown']/df['cum_roll_max']).max()
    
#%% Monthly Data collection:List of all the stocks in SPY as of feb-2-2023. We will assume that the list was almost same 10y back
'''
my_portfolio = ["AAPL","LCID","RIVN","TSLA","AMZN","NFLX","NDAQ","GNRC","NET","ACI",
           "GOOGL","META","SNAP","SPY","XSD","INTC","HOOD","DUOL","TEAM","ASML",
           "MSFT","VZ"]
'''

my_portfolio = []

SPY_universe = ["AAPL",
"MSFT",
"AMZN",
"GOOGL",
"GOOG",
"BRK-B",
"NVDA",
"TSLA",
"XOM",
"UNH",
"JNJ",
"META",
"JPM",
"V",
"HD",
"PG",
"MA",
"CVX",
"MRK",
"MRNA",
"LLY",
"ABBV",
"BAC",
"PFE",
"AVGO",
"KO",
"PEP",
"COST",
"TMO",
"DIS",
"WMT",
"CSCO",
"ABT",
"MCD",
"ACN",
"ADBE",
"WFC",
"CMCSA",
"DHR",
"VZ",
"CRM",
"TXN",
"LIN",
"NFLX",
"NKE",
"PM",
"BMY",
"QCOM",
"NEE",
"T",
"RTX",
"AMD",
"UPS",
"HON",
"COP",
"LOW",
"ORCL",
"AMGN",
"UNP",
"MS",
"SPGI",
"INTU",
"CAT",
"GS",
"SBUX",
"INTC",
"PLD",
"IBM",
"BA",
"SCHW",
"MDT",
"BLK",
"ELV",
"CVS",
"DE",
"AMAT",
"LMT",
"AMT",
"AXP",
"GILD",
"C",
"PYPL",
"NOW",
"BKNG",
"ADP",
"SYK",
"TJX",
"ADI",
"ISRG",
"CI",
"GE",
"MDLZ",
"TMUS",
"CB",
"MMC",
"MO",
"TGT",
"REGN",
"ZTS",
"PGR",
"DUK",
"VRTX",
"SO",
"SLB",
"LRCX",
"EOG",
"BDX",
"ITW",
"EQIX",
"BSX",
"MU",
"CSX",
"FISV",
"PNC",
"TFC",
"AON",
"MMM",
"USB",
"CCI",
"APD",
"ETN",
"NOC",
"CME",
"FCX",
"HUM",
"EL",
"CL",
"ICE",
"NSC",
"GM",
"KLAC",
"SHW",
"F",
"WM",
"MPC",
"SNPS",
"HCA",
"ATVI",
"EMR",
"MCK",
"PXD",
"EW",
"DG",
"GD",
"MCO",
"CDNS",
"D",
"FDX",
"VLO",
"NXPI",
"SRE",
"ORLY",
"ADSK",
"PSA",
"APH",
"AEP",
"MAR",
"PSX",
"CMG",
"COF",
"MET",
"AZO",
"MCHP",
"A",
"FIS",
"NUE",
"ROP",
"MSCI",
"OXY",
"ADM",
"GIS",
"IQV",
"JCI",
"CHTR",
"AIG",
"KMB",
"TEL",
"PH",
"TRV",
"TT",
"DOW",
"SPG",
"O",
"MSI",
"DXCM",
"IDXX",
"BIIB",
"EXC",
"NEM",
"CNC",
"AJG",
"ROST",
"LHX",
"HLT",
"DVN",
"CARR",
"AFL",
"MNST",
"SYY",
"ECL",
"WMB",
"PCAR",
"PAYX",
"HES",
"CTAS",
"PRU",
"XEL",
"STZ",
"AMP",
"DD",
"BK",
"TDG",
"KMI",
"CTSH",
"YUM",
"WELL",
"CMI",
"ALL",
"MTD",
"ON",
"ILMN",
"FTNT",
"OTIS",
"HAL",
"WBD",
"DLR",
"HSY",
"ALB",
"ODFL",
"STT",
"ED",
"ROK",
"RMD",
"SBAC",
"VICI",
"DLTR",
"AME",
"ANET",
"KEYS",
"CSGP",
"DHI",
"APTV",
"DFS",
"GPN",
"URI",
"KHC",
"BKR",
"PPG",
"FAST",
"PEG",
"ENPH",
"OKE",
"EA",
"GWW",
"WEC",
"CPRT",
"KDP",
"IFF",
"KR",
"VRSK",
"AWK",
"TROW",
"ES",
"CBRE",
"EBAY",
"EFX",
"HPQ",
"CEG",
"WTW",
"IT",
"LEN",
"GLW",
"MTB",
"CDW",
"WBA",
"ULTA",
"FRC",
"ZBH",
"WY",
"EIX",
"ALGN",
"FITB",
"AVB",
"ABC",
"TSCO",
"DAL",
"ARE",
"PCG",
"RSG",
"VMC",
"LYB",
"FANG",
"ANSS",
"GPC",
"FTV",
"HIG",
"BAX",
"LH",
"MLM",
"ACGL",
"DOV",
"RF",
"AEE",
"IR",
"ETR",
"EQR",
"FE",
"HBAN",
"DTE",
"STE",
"LUV",
"EXR",
"CFG",
"EPAM",
"PPL",
"PFG",
"PWR",
"HPE",
"HOLX",
"RJF",
"MPWR",
"VTR",
"STLD",
"VRSN",
"WST",
"WAT",
"NDAQ",
"NTRS",
"TDY",
"CAH",
"MAA",
"INVH",
"CTRA",
"EXPD",
"SIVB",
"CHD",
"WAB",
"BALL",
"TSN",
"XYL",
"LVS",
"MKC",
"OMC",
"ETSY",
"CNP",
"KEY",
"BBY",
"CINF",
"AMCR",
"CMS",
"SWKS",
"EXPE",
"DRI",
"BR",
"PKI",
"SEDG",
"TTWO",
"ZBRA",
"MOH",
"COO",
"MOS",
"AES",
"TER",
"K",
"CAG",
"PAYC",
"UAL",
"CLX",
"SYF",
"IEX",
"DGX",
"CF",
"TRGP",
"FSLR",
"POOL",
"NVR",
"MRO",
"FLT",
"ATO",
"JBHT",
"IRM",
"FDS",
"FMC",
"J",
"SJM",
"TXT",
"GRMN",
"INCY",
"AVY",
"TRMB",
"NTAP",
"LKQ",
"ESS",
"RCL",
"IPG",
"PEAK",
"IP",
"HWM",
"MTCH",
"VTRS",
"AKAM",
"TYL",
"EVRG",
"MKTX",
"SWK",
"KIM",
"STX",
"LW",
"PHM",
"PTC",
"WDC",
"APA",
"SNA",
"PKG",
"UDR",
"WRB",
"BRO",
"GEN",
"LNT",
"NDSN",
"HST",
"MGM",
"RE",
"CPT",
"LDOS",
"JKHY",
"HRL",
"CRL",
"CHRW",
"DPZ",
"KMX",
"MAS",
"CBOE",
"PARA",
"CE",
"TECH",
"HSIC",
"TFX",
"CDAY",
"L",
"CCL",
"TPR",
"EQT",
"LYV",
"BWA",
"CZR",
"EMN",
"NI",
"QRVO",
"BXP",
"AAL",
"ALLE",
"WYNN",
"BBWI",
"GL",
"BIO",
"REG",
"CPB",
"TAP",
"JNPR",
"CTLT",
"UHS",
"VFC",
"PNR",
"CMA",
"RHI",
"AAP",
"FFIV",
"BEN",
"IVZ",
"AOS",
"WRK",
"SBNY",
"PNW",
"HII",
"WHR",
"XRAY",
"ROL",
"NWSA",
"FRT",
"SEE",
"NRG",
"GNRC",
"ZION",
"HAS",
"OGN",
"AIZ",
"NCLH",
"DXC",
"ALK",
"MHK",
"NWL",
"LNC",
"RL",
"LUMN",
"FOX",
"FOXA",
"DVA",
"DISH",
"NWS"]
SPY_universe.sort()

# add my portfolio stock and SPY stocks in tickers and removing duplocates. 
tickers = my_portfolio + [x for x in SPY_universe if x not in my_portfolio]

ohlcv_data = {}


# Creating a dictionary where key is the ticker name and value is the dataframe with ohlcv_data
for ticker in tickers:
    temp = yf.download(ticker,period='10y',interval='1mo')
    temp.dropna(how='any',inplace=True)
    ohlcv_data[ticker] = temp
tickers = ohlcv_data.keys()
    
#%% calculating KPIs for Index buy and hold strategy over the same period

SPY = yf.download("SPY",period='10y',interval='1mo')
SPY["mon_return"] = SPY["Adj Close"].pct_change().fillna(0)
print("SPY CAGR:{}".format( CAGR(SPY)))
print("SPY Sharpe:{}" .format(sharpe(SPY,0.025)))
print("SPY Max_dd:{}" .format(max_dd(SPY)))

#%% Backtesting: Calculating monthly return for each stock and consolidating return info by stock in a separate dataframe

ohlcv_dict = copy.deepcopy(ohlcv_data)
return_df = pd.DataFrame()
for ticker in tickers:
    print("calculating monthly return for ",ticker)
    ohlcv_dict[ticker]["mon_return"] = ohlcv_dict[ticker]["Adj Close"].pct_change()
    return_df[ticker] = ohlcv_dict[ticker]["mon_return"]   
return_df.drop(return_df.index[0], inplace=True)
return_df.dropna(inplace=True,axis=1)

# function to calculate portfolio return iteratively
def pflio(DF,m,x):
    """Returns cumulative portfolio return
    DF = dataframe with monthly return info for all stocks
    m = number of stock in the portfolio
    x = number of underperforming stocks to be removed from portfolio monthly"""
    df = DF.copy()
    portfolio = []
    monthly_ret = [0]
    for i in range(len(df)-1):
        if len(portfolio) > 0:
            monthly_ret.append(df[portfolio].iloc[i,:].mean())
            print("Month's return:",monthly_ret[i])
            bad_stocks = df[portfolio].iloc[i,:].sort_values(ascending=True)[:x].index.values.tolist()
            portfolio = [t for t in portfolio if t not in bad_stocks]
        fill = m - len(portfolio)
        new_picks = df.iloc[i,:].sort_values(ascending=False)[:fill].index.values.tolist()
        portfolio = portfolio + new_picks
        print("----------------------")
        print("Portfolio for:",df.index[i+1])
        print(portfolio)
    monthly_ret_df = pd.DataFrame(np.array(monthly_ret),columns=["mon_return"])
    print('\n')
    print("Current portfolio",portfolio)
    return monthly_ret_df

#%% Calculating overall strategy's KPIs
'''
grid = pd.DataFrame()
for i in range(0,100):
    print(i)
    for j in range(0,i):
        grid.loc[i,j] = CAGR(pflio(return_df,i,j))
grid = grid.fillna(0)  
max_value = grid.values.max()  
'''
 
CAGR(pflio(return_df,2,1))
sharpe(pflio(return_df,2,1),0.025)
max_dd(pflio(return_df,2,1)) 

#%% Visualization
fig, ax = plt.subplots()
plt.plot((1+pflio(return_df,2,1)).cumprod())
plt.plot((1+SPY["mon_return"].reset_index(drop=True)).cumprod())
plt.title("Index Return vs Strategy Return")
plt.ylabel("cumulative return")
plt.xlabel("months")
ax.legend(["Strategy Return","Index Return"])
    
    
    
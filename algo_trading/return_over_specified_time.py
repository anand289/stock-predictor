#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 11:09:26 2023

@author: anandsingh

Calcualtes return over a specified time  arranges them in ascending order
"""

import pandas as pd
import yfinance as yf
import datetime as datetime

#%%

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



# List of stocks we need the data for
tickers = SPY_universe

ohlcv_data = {}
returns = pd.Series()

start = datetime.datetime(year=2023, month=6, day=1)
end = datetime.datetime(year=2023, month=6, day=30)
#end =  datetime.datetime.now()

# Creating a dictionary where key is the ticker name and value is the dataframe with ohlcv_data
for ticker in tickers:
    temp = yf.download(ticker,start,end)
    temp.dropna(how='any',inplace=True)
    ohlcv_data[ticker] = temp
#%%

def cal_return(DF):
    df = DF.copy()
    ret = (df.iloc[-1]['Adj Close']-df.iloc[0]['Open'])/df.iloc[0]['Open']
    return ret
#%% THis section will give error, run the next section regardless

for ticker in ohlcv_data:
    returns[ticker] = cal_return(ohlcv_data[ticker])
    
#%%
sorted_returns = returns.sort_values(ascending=False)
print(sorted_returns)

#%% Running

mon_1 = "NVDA"
mon_2 = "CMG"

current_stocks = ["SPY",mon_1,mon_2]

tickers = current_stocks

ohlcv_data = {}
returns = pd.Series()

start = datetime.datetime(year=2023, month=6, day=1)
end = datetime.datetime(year=2023, month=6, day=30)
#end =  datetime.datetime.now()

# Creating a dictionary where key is the ticker name and value is the dataframe with ohlcv_data
for ticker in tickers:
    temp = yf.download(ticker,start,end)
    temp.dropna(how='any',inplace=True)
    ohlcv_data[ticker] = temp
 

def cal_return(DF):
    df = DF.copy()
    ret = (df.iloc[-1]['Adj Close']-df.iloc[0]['Open'])/df.iloc[0]['Open']
    return ret

#%%

for ticker in ohlcv_data:
    returns[ticker] = cal_return(ohlcv_data[ticker])
    

sorted_returns = returns.sort_values(ascending=False)
print(sorted_returns)

total_return = (sorted_returns["NVDA"] + sorted_returns["CMG"])/2 - sorted_returns["SPY"]
print(total_return)
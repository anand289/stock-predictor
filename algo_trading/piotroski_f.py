# ============================================================================
# Piotroski f score implementation
#F score --> Works best for mid-cap and small-cap companies

# Please report bugs/issues in the Q&A section
# =============================================================================

import pandas as pd


my_portfolio = ["LCID","RIVN","AAPL","TSLA","AMZN","NFLX","NDAQ","GNRC","NET","ACI",
           "GOOGL","META","SNAP","SPY","XSD","INTC","HOOD","DUOL","TEAM","ASML",
           "MSFT","VZ"]

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

# add my portfolio stock and SPY stocks in tickers and removing duplocates. 
tickers = my_portfolio + [x for x in SPY_universe if x not in my_portfolio]


#list of tickers whose financial data needs to be extracted
financial_dir = {} #directory to store financial information for each ticker

for ticker in tickers:
    try:
        print("scraping financial statement data for ",ticker)
        #getting balance sheet data
        url = "https://stockrow.com/api/companies/{}/financials.xlsx?dimension=A&section=Balance%20Sheet&sort=desc".format(ticker)
        df1 = pd.read_excel(url)
        #getting income statement data
        url = "https://stockrow.com/api/companies/{}/financials.xlsx?dimension=A&section=Income%20Statement&sort=desc".format(ticker)
        df2 = pd.read_excel(url)
        #getting cashflow statement data
        url = "https://stockrow.com/api/companies/{}/financials.xlsx?dimension=A&section=Cash%20Flow&sort=desc".format(ticker)
        df3 = pd.read_excel(url)
        #combining all extracted information with the corresponding ticker
        df = pd.concat([df1,df2,df3])
        columns = df.columns.values
        for i in range(len(columns)):
            if columns[i] == "Unnamed: 0":
                columns[i] = "heading"
            else:
                columns[i] = columns[i].strftime("%Y-%m-%d")
        df.columns = columns
        df.set_index("heading",inplace=True)
        financial_dir[ticker] = df
    except Exception as e:
        print(ticker,":", e)


# selecting relevant financial information for each stock using fundamental data
stats = ["Net Income Common",
         "Total Assets",
         "Operating Cash Flow",
         "Long Term Debt (Total)",
         "Total non-current liabilities",
         "Total current assets",
         "Total current liabilities",
         "Common Equity (Total)",
         "Revenue",
         "Gross Profit"] # change as required

indx = ["NetIncome","TotAssets","CashFlowOps","LTDebt","TotLTLiab",
        "CurrAssets","CurrLiab","CommStock","TotRevenue","GrossProfit"]


def info_filter(df,stats,indx,lookback):
    """function to filter relevant financial information
       df = dataframe to be filtered
       stats = headings to filter
       indx = rename long headings
       lookback = number of years of data to be retained"""
    df_new = df.loc[stats,df.columns[:3]]
    df_new.rename(dict(zip(stats,indx)),inplace=True)
    df_new.loc["OtherLTDebt",:] = df_new.loc["TotLTLiab",:] - df_new.loc["LTDebt",:]
    return df_new

#applying filtering to the finacials
transformed_df = {}
for ticker in financial_dir:
    transformed_df[ticker] = info_filter(financial_dir[ticker],stats,indx,3)


def piotroski_f(df_dict):
    """function to calculate f score of each stock and output information as dataframe"""
    f_score = {}
    for ticker in df_dict:
        columns = df_dict[ticker].columns
        ROA_FS = int(df_dict[ticker].loc["NetIncome",columns[0]]/((df_dict[ticker].loc["TotAssets",columns[0]] + df_dict[ticker].loc["TotAssets",columns[1]])/2) > 0)
        CFO_FS = int(df_dict[ticker].loc["CashFlowOps",columns[0]] > 0)
        ROA_D_FS = int((df_dict[ticker].loc["NetIncome",columns[0]]/((df_dict[ticker].loc["TotAssets",columns[0]] + df_dict[ticker].loc["TotAssets",columns[1]])/2)) > (df_dict[ticker].loc["NetIncome",columns[1]]/((df_dict[ticker].loc["TotAssets",columns[1]] + df_dict[ticker].loc["TotAssets",columns[2]])/2)))
        CFO_ROA_FS = int(df_dict[ticker].loc["CashFlowOps",columns[0]]/df_dict[ticker].loc["TotAssets",columns[0]] > df_dict[ticker].loc["NetIncome",columns[0]]/((df_dict[ticker].loc["TotAssets",columns[0]] + df_dict[ticker].loc["TotAssets",columns[1]])/2))
        LTD_FS = int((df_dict[ticker].loc["LTDebt",columns[0]] + df_dict[ticker].loc["OtherLTDebt",columns[0]]) < (df_dict[ticker].loc["LTDebt",columns[1]] + df_dict[ticker].loc["OtherLTDebt",columns[1]]))
        CR_FS = int((df_dict[ticker].loc["CurrAssets",columns[0]] / df_dict[ticker].loc["CurrLiab",columns[0]]) > (df_dict[ticker].loc["CurrAssets",columns[1]] / df_dict[ticker].loc["CurrLiab",columns[1]]))
        DILUTION_FS = int(df_dict[ticker].loc["CommStock",columns[0]] <= df_dict[ticker].loc["CommStock",columns[1]])
        GM_FS = int((df_dict[ticker].loc["GrossProfit",columns[0]]/df_dict[ticker].loc["TotRevenue",columns[0]]) > (df_dict[ticker].loc["GrossProfit",columns[1]]/df_dict[ticker].loc["TotRevenue",columns[1]]))
        ATO_FS = int((df_dict[ticker].loc["TotRevenue",columns[0]]/((df_dict[ticker].loc["TotAssets",columns[0]] + df_dict[ticker].loc["TotAssets",columns[1]])/2)) > (df_dict[ticker].loc["TotRevenue",columns[1]]/((df_dict[ticker].loc["TotAssets",columns[1]] + df_dict[ticker].loc["TotAssets",columns[2]])/2)))
        f_score[ticker] = [ROA_FS,CFO_FS,ROA_D_FS,CFO_ROA_FS,LTD_FS,CR_FS,DILUTION_FS,GM_FS,ATO_FS]
    f_score_df = pd.DataFrame(f_score,index=["PosROA","PosCFO","ROAChange","Accruals","Leverage","Liquidity","Dilution","GM","ATO"])
    return f_score_df

# sorting stocks with highest Piotroski f score to lowest
f_score_df = piotroski_f(transformed_df)
f_score_df.sum().sort_values(ascending=False)




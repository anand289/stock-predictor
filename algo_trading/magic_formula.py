# ============================================================================
# Greenblatt's Magic Formula Implementation
# Author - Mayank Rasu

# Please report bugs/issues in the Q&A section
# =============================================================================

import requests
from bs4 import BeautifulSoup
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
financial_dir = {}

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
        
        #getting key statistics data --> Market Cap (Intraday)
        temp_dir = {}
        url = 'https://finance.yahoo.com/quote/'+ticker+'/key-statistics?p='+ticker
        headers={'User-Agent': "Chrome/109.0.5414.87"}
        page = requests.get(url, headers=headers)
        page_content = page.content
        soup = BeautifulSoup(page_content,'html.parser')
        tabl = soup.findAll("div", {"class":"Fl(start) smartphone_W(100%) W(100%)"}) # try to remove the leading space if the code breaks "class": "W(100%) Bdcl(c)"
        for t in tabl:
            rows = t.find_all("tr")
            for row in rows:
                if len(row.get_text(separator='|').split("|")[0:2])>0:
                    temp_dir[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[2]
        df4 = pd.DataFrame(temp_dir.items(),columns=df3.columns[0:2])
        df4.iloc[:,1] = df4.iloc[:,1].replace({'M': 'E+03','B': 'E+06','T': 'E+09','%': 'E-02'}, regex=True)
        df4.iloc[:,1] = pd.to_numeric(df4.iloc[:,1],errors="coerce")
        df4 = df4[df4["Unnamed: 0"].isin(["Market Cap (intraday)"])]
        
        #getting key statistics data --> Forward Annual Dividend Yield
        tabl_2 = soup.findAll("table", {"class": "W(100%) Bdcl(c)"}) # try to remove the leading space if the code breaks "class": "W(100%) Bdcl(c)"
        for t in tabl_2:
            rows = t.find_all("tr")
            for row in rows:
                if len(row.get_text(separator='|').split("|"))>3:
                    temp_dir[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[3]
        df5 = pd.DataFrame(temp_dir.items(),columns=df3.columns[0:2])
        df5.iloc[:,1] = df5.iloc[:,1].replace({'M': 'E+03','B': 'E+06','T': 'E+09','%': 'E-02'}, regex=True)
        df5.iloc[:,1] = pd.to_numeric(df5.iloc[:,1],errors="coerce")
        df5 = df5[df5["Unnamed: 0"].isin(["Forward Annual Dividend Yield"])]
        
        #combining all extracted information with the corresponding ticker
        df = pd.concat([df1,df2,df3,df4,df5]).iloc[:,[0,1]]
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


# creating dataframe with relevant financial information for each stock using fundamental data
stats = ["EBITDA",
         "Depreciation & Amortization",
         "Market Cap (intraday)",
         "Net Income Common",
         "Operating Cash Flow",
         "Capital expenditures",
         "Total current assets",
         "Total current liabilities",
         "Property, Plant, Equpment (Net)",
         "Shareholders Equity (Total)",
         "Long Term Debt (Total)",
         "Forward Annual Dividend Yield"] # change as required

indx = ["EBITDA","D&A","MarketCap","NetIncome","CashFlowOps","Capex","CurrAsset",
        "CurrLiab","PPE","BookValue","TotDebt","DivYield"]

def info_filter(df,stats,indx):
    """function to filter relevant financial information
       df = dataframe to be filtered
       stats = headings to filter
       indx = rename long headings
       lookback = number of years of data to be retained"""
    for stat in stats:
        if stat not in df.index:
            print(stat)
            return
    df_new = df.loc[stats,:]
    df_new.rename(dict(zip(stats,indx)),inplace=True)
    return df_new

#applying filtering to the finacials and calculating relevant financial metrics for each stock
transformed_df = {}
for ticker in financial_dir:
    transformed_df[ticker] = info_filter(financial_dir[ticker],stats,indx)
    if transformed_df[ticker] is None:
        del transformed_df[ticker]
        continue
    transformed_df[ticker].loc["EBIT",:] = transformed_df[ticker].loc["EBITDA",:] - transformed_df[ticker].loc["D&A",:]
    transformed_df[ticker].loc["TEV",:] =  transformed_df[ticker].loc["MarketCap",:] + \
                                           transformed_df[ticker].loc["TotDebt",:] - \
                                           (transformed_df[ticker].loc["CurrAsset",:]-transformed_df[ticker].loc["CurrLiab",:])
    transformed_df[ticker].loc["EarningYield",:] =  transformed_df[ticker].loc["EBIT",:]/transformed_df[ticker].loc["TEV",:]
    transformed_df[ticker].loc["FCFYield",:] = (transformed_df[ticker].loc["CashFlowOps",:]-transformed_df[ticker].loc["Capex",:])/transformed_df[ticker].loc["MarketCap",:]
    transformed_df[ticker].loc["ROC",:]  = (transformed_df[ticker].loc["EBITDA",:] - transformed_df[ticker].loc["D&A",:])/(transformed_df[ticker].loc["PPE",:]+transformed_df[ticker].loc["CurrAsset",:]-transformed_df[ticker].loc["CurrLiab",:])
    transformed_df[ticker].loc["BookToMkt",:] = transformed_df[ticker].loc["BookValue",:]/transformed_df[ticker].loc["MarketCap",:]

################################Output Dataframes##############################
final_stats_val_df = pd.DataFrame(columns=transformed_df.keys())
for key in transformed_df:
    final_stats_val_df[key] = transformed_df[key].values.flatten()
    final_stats_val_df.set_index(transformed_df[key].index,inplace=True)
    

# finding value stocks based on Magic Formula
final_stats_val_df.loc["CombRank",:] = final_stats_val_df.loc["EarningYield",:].rank(ascending=False,na_option='bottom')+final_stats_val_df.loc["ROC",:].rank(ascending=False,na_option='bottom')
final_stats_val_df.loc["MagicFormulaRank",:] = final_stats_val_df.loc["CombRank",:].rank(method='first')
value_stocks = final_stats_val_df.loc["MagicFormulaRank",:].sort_values()
print("------------------------------------------------")
print("Value stocks based on Greenblatt's Magic Formula")
print(value_stocks)


# finding highest dividend yield stocks
high_dividend_stocks = final_stats_val_df.loc["DivYield",:].sort_values(ascending=False)
print("------------------------------------------------")
print("Highest dividend paying stocks")
print(high_dividend_stocks)

# # Magic Formula & Dividend yield combined
final_stats_val_df.loc["CombinedRank",:] =  final_stats_val_df.loc["EarningYield",:].rank(ascending=False,method='first') \
                                           +final_stats_val_df.loc["ROC",:].rank(ascending=False,method='first')  \
                                           +final_stats_val_df.loc["DivYield",:].rank(ascending=False,method='first')
value_high_div_stocks = final_stats_val_df.T.sort_values("CombinedRank").loc[:,["EarningYield","ROC","DivYield","CombinedRank"]]
print("------------------------------------------------")
print("Magic Formula and Dividend Yield combined")
print(value_high_div_stocks)

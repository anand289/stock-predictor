#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 18:52:49 2023

@author: anandsingh
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import pandas  as pd
import time
import string
import nltk

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

driver = webdriver.Chrome('/Users/anandsingh/Desktop/Personal/Udemy_Courses/Web_Scraping/chromedriver')

url = 'https://www.nasdaq.com/market-activity/stocks/tsla/news-headlines'

driver.get(url)

articles_skipped = 0
list_of_dates = []
list_of_articles = []
list_of_compounds = []
symbols =  list(string.punctuation)

pages_to_check = 100

for p in range(0,pages_to_check):
    
    number_of_headlines_per_page = driver.find_elements(By.XPATH,'/html/body/div[3]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/ul/li')
    
    for i in range(1,len(number_of_headlines_per_page)+1):
        main_page_headline = driver.find_element(By.XPATH,'/html/body/div[3]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/ul/li['+str(i)+']/a')
        headline_link = main_page_headline.get_attribute('href')
        print(main_page_headline.text)
        
        
        
        try:
            headline_article = requests.get(headline_link, headers={'User-Agent': 'Custom'})
            soup = BeautifulSoup(headline_article.text,'lxml')
        except:
            articles_skipped += 1
            continue
            
        
        try:
            date = soup.find('p',{'class':'jupiter22-c-author-byline__timestamp' }).text.split(" — ")[0]
            date = datetime.strptime(date, '%B %d, %Y').strftime('%m/%d/%y')
        except:
            continue   
        print(date)
        

        paragraphs_raw = soup.find_all('p')
        paragraphs = []
        article = []
        
        paragraphs.append(main_page_headline.text.split('\n')[1])
        for i in range (0,len(paragraphs_raw)):
            if "The views and opinions expressed herein are the views and opinions of the author and do not necessarily reflect those of Nasdaq, Inc." in paragraphs_raw[i]:
                break
            if (paragraphs_raw[i].text != "") and ("\n" not in paragraphs_raw[i].text):        
                    if len(paragraphs_raw[i]):
                        paragraphs.append(paragraphs_raw[i].text)       
        article = ' '.join(paragraphs)
            
        list_of_dates.append(date)    
        list_of_articles.append(article)
        list_of_compounds.append(sid.polarity_scores(article).get('compound'))
    
        
                
    # clicking the next page arrow button    
    driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div[3]/button[2]"))))
    time.sleep(3)
#%% Group all the data by date

tesla_article_table = pd.DataFrame({'Date': list_of_dates, 'Articles': list_of_articles, 'SA': list_of_compounds })
tesla_article_table_grouped = tesla_article_table.groupby('Date',sort=False).mean()

# Adding Day coloum in the table
Day = []
for i in tesla_article_table_grouped.index:
    Day.append(datetime.strptime(i, "%m/%d/%y").strftime("%A"))   
tesla_article_table_grouped['Day'] = Day 

for i in range(0,len(tesla_article_table_grouped.index)):
    # 0 --> SA
    # 1 --> Day
    if tesla_article_table_grouped.iloc[i,1] == 'Monday':
        try: #SA of Monday is average of SA of previous saturday and sunday
            tesla_article_table_grouped.iloc[i,0] = (tesla_article_table_grouped.iloc[i,0]+tesla_article_table_grouped.iloc[i+1,0]+tesla_article_table_grouped.iloc[i+2,0])/3
        except: #Table might end on Monday and have undefined Sunday or Saturday values
            continue
        
        
        

#%% Import data from CSV
tesla_stocks_table = pd.read_csv('/Users/anandsingh/Desktop/Udemy_Courses/Web_Scraping/Tesla/Tesla_data.csv',index_col=0)
tesla_stocks_table_only_change = tesla_stocks_table .drop(['Close/Last','Volume','Open','High','Low'],axis=1)



#%% Concatenate article compound values (tesla_article_table_grouped) with price change data (tesla_article_table_only_change)

concatenated_table = pd.concat([tesla_article_table_grouped,tesla_stocks_table_only_change],axis=1).dropna(axis=0) 
concatenated_table['Change'] = concatenated_table['Change'].shift(1)
concatenated_table.dropna(inplace = True)
print(concatenated_table['SA'].corr(concatenated_table['Change']))




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

start_time = datetime.now()

# for sentiment analysis of the articles
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

# driver to run selenium 
driver = webdriver.Chrome('/Users/anandsingh/Desktop/Personal/Udemy_Courses/Web_Scraping/chromedriver')

#location from where articles will be scrapped
url = 'https://www.nasdaq.com/market-activity/stocks/tsla/news-headlines'

driver.get(url)


articles_skipped = 0 #if there is an error in reading an article code will skip that article without throwing an error, and record the number of skipped articles in this counter.
list_of_dates = [] # will be populated by a coloum values of all the dates.
list_of_articles = [] # to store all the articles' text in a coloum
list_of_compounds = [] 
list_of_positives = []
list_of_negatives = []
list_of_neutrals = []
symbols =  list(string.punctuation) #to eleminate all the stop words if needed

pages_to_check = 1249

# to loop through all the pages
for p in range(0,pages_to_check):
    
    # number of article on a single page
    number_of_headlines_per_page = driver.find_elements(By.XPATH,'/html/body/div[3]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/ul/li')
    
    # to loop throuhg all the articles in a page
    for i in range(1,len(number_of_headlines_per_page)+1):
        main_page_headline = driver.find_element(By.XPATH,'/html/body/div[3]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/ul/li['+str(i)+']/a')
        headline_link = main_page_headline.get_attribute('href')
        print(main_page_headline.text) # prints article headline
        
        
        # saves the whole article text in a variable called 'soup'
        try:
            headline_article = requests.get(headline_link, headers={'User-Agent': 'Custom'})
            soup = BeautifulSoup(headline_article.text,'lxml')
        except:
            articles_skipped += 1
            continue
            
        # saves the date in a varible called 'date'
        try:
            date = soup.find('p',{'class':'jupiter22-c-author-byline__timestamp' }).text.split(" — ")[0]
            date = datetime.strptime(date, '%B %d, %Y').strftime('%m/%d/%y')
        except:
            continue   
        print(date)
        
        # pragraphs_raw stores all the paragraghs (anything that has tag 'p') as in the html
        paragraphs_raw = soup.find_all('p')
        
        # pragraphs will store only clean texts from paragraphs_raw
        paragraphs = []
        
        # article will join all the paragraphs
        article = []
        
        paragraphs.append(main_page_headline.text.split('\n')[1])
        
        # loop to store clean paragraphs from 'paragrahs_raw' to 'paragraphs'
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
        list_of_positives.append(sid.polarity_scores(article).get('pos'))
        list_of_negatives.append(sid.polarity_scores(article).get('neg'))
        list_of_neutrals.append(sid.polarity_scores(article).get('neu'))
    
        
                
    # clicking the next page arrow button    
    driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div[3]/button[2]"))))
    time.sleep(3)
    
    end_time = datetime.now()
    print("Total run time: ",end_time-start_time)
#%% Create a table with coloums "Date" "Articles" and "SA compound values"
#Group all the data by "Date"

tesla_article_table = pd.DataFrame({'Date': list_of_dates, 'Articles': list_of_articles, 'compound': list_of_compounds,'pos': list_of_positives ,'neg': list_of_negatives,'neu': list_of_neutrals  })
tesla_article_table_grouped = tesla_article_table.groupby('Date',sort=False).mean()

#%% Section to add weekend "SA compound values" to Monday. 

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

tesla_stocks_table = pd.read_csv('/Users/anandsingh/Desktop/stock_predictor/Tesla/Tesla_data.csv',index_col=0)
tesla_stocks_table_only_change = tesla_stocks_table .drop(['Close/Last','Volume','Open','High','Low'],axis=1)


#%% Concatenate article compound values (tesla_article_table_grouped) with price change data (tesla_article_table_only_change)

concatenated_table = pd.concat([tesla_article_table_grouped,tesla_stocks_table_only_change],axis=1).dropna(axis=0) 
concatenated_table['Change'] = concatenated_table['Change'].shift(1)
concatenated_table.dropna(inplace = True)

print("Change vs Compound_score: ",concatenated_table['compound'].corr(concatenated_table['Change']))
print("Change vs Positive_score: ",concatenated_table['pos'].corr(concatenated_table['Change']))
print("Change vs Negative_score: ",concatenated_table['neg'].corr(concatenated_table['Change']))
print("Change vs Neutral_score: ",concatenated_table['neu'].corr(concatenated_table['Change']))



#%% Export "tesla_article_table" and  "concatenated_data"

#tesla_article_table.to_excel('/Users/anandsingh/Desktop/stock_predictor/Tesla/results/tesla_article_table.xlsx')
#concatenated_table.to_excel('/Users/anandsingh/Desktop/stock_predictor/Tesla/results/concatenated_table.xlsx')



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 11:51:40 2022

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


driver = webdriver.Chrome('/Users/anandsingh/Desktop/Personal/Udemy_Courses/Web_Scraping/chromedriver')

url = 'https://www.nasdaq.com/market-activity/stocks/tsla/news-headlines'

driver.get(url)

articles_skipped = 0
list_of_dates = []
list_of_words = []
number_of_words = []
symbols = ['~', ':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', '<', '`', '}', '.', '_', '=', ']', '!', '>', ';', '?', '#', '$', ')', '/']
#symbols =  string.punctuation

pages_to_check = 1249


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
        
        
        article = soup.find_all('p')
        
        words = []
        for i in article[5:len(article)-5]:
            string = i.text.split()
            for word in string:
                if word.isalpha():
                    if len(word)>2:
                        word = word.lower()
                        words.append(word)
                elif word[-1] in symbols:
                    if len(word)>3:
                        word = word.strip(word[-1])
                        word = word.lower()
                        words.append(word)
                
                
        list_of_dates.append(date)    
        list_of_words.append(words)
        number_of_words.append(len(words))   
    
    # clicking the next page arrow button    
    driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div[3]/button[2]"))))
    time.sleep(3)
    
print('\a') #for ringing a bell here
    
#%% Creating a table with "Date" "List of all words appearing on that date" "size"
 
tesla_words_table = pd.DataFrame({'Date': list_of_dates, 'Words appeared on this day': list_of_words, 'Size': number_of_words })
tesla_words_table_grouped = tesla_words_table.groupby('Date',sort=False).agg({'Words appeared on this day':'sum','Size':'sum'})

#%% Calculating frequency of occurance of each word per day

table_of_frequencies = pd.DataFrame()

for i in range(0,len(tesla_words_table_grouped)):
    words_on_day = tesla_words_table_grouped.iloc[i]['Words appeared on this day']
    frequencies = {}

    # iterating over the list
    for item in words_on_day:
       # checking the element in dictionary
       if item in frequencies:
          # incrementing the counr
          frequencies[item] += 1
       else:
          # initializing the count
          frequencies[item] = 1
    sorted_frequency = dict(sorted(frequencies.items(), key=lambda x:x[1]))
    sorted_frequency_df = pd.DataFrame(sorted_frequency, index = [tesla_words_table_grouped.index[i]])
    table_of_frequencies = pd.concat([table_of_frequencies,sorted_frequency_df])
    table_of_frequencies = table_of_frequencies.fillna(0)
    

#%% Adding data table and concatenating with table_of_frequencies

frequencies = table_of_frequencies.transpose()
frequencies.to_excel('/Users/anandsingh/Desktop/Personal/Udemy_Courses/Web_Scraping/table_of_frequencies_1249.xlsx')

tesla_stocks_table = pd.read_csv('/Users/anandsingh/Desktop/Personal/Udemy_Courses/Web_Scraping/TeslaData_12_10.csv', index_col=0)
tesla_stocks_table_only_change = tesla_stocks_table .drop(['Close/Last','Volume','Open','High','Low'],axis=1)


concatenated_table = pd.concat([table_of_frequencies,tesla_stocks_table_only_change],axis=1)
concatenated = concatenated_table.transpose()
concatenated.to_excel('/Users/anandsingh/Desktop/Personal/Udemy_Courses/Web_Scraping/concatenated_table_1249.xlsx')
#%% Finding corelation between to tables and exporting it

#corelation_matrix = concatenated_table.corrwith(concatenated_table['Percentage_change'])
#corelation = corelation_matrix.transpose()
#corelation.to_excel('/Users/anandsingh/Desktop/Personal/Udemy_Courses/Web_Scraping/tesla_corelation_889.xlsx')

#%%
''' Improvements needed in the code:
    1. Articles over the weekend should be added to Monday.
    2. Change coloumn needs to  be shifted one up --> To account for previous day's news
'''

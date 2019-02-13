from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium
import time


from bs4 import BeautifulSoup
import requests

import pandas as pd
import numpy as np



browser = webdriver.Chrome('/Users/taylorphillips/galvanize/capstone/chromedriver')
browser.get("https://secure.conservation.ca.gov/WellSearch")

webpage = requests.get('https://secure.conservation.ca.gov/WellSearch/?ActiveWell=True&ActiveOp=True&District=4&Command=Search&PgStart=0&PgLength=10&SortCol=6&SortDir=asc')

bs_obj = BeautifulSoup(webpage.text, 'html.parser')
#browser.find_element_by_xpath("//*[@id='select2-results-1']/li[4]").click()
print("Select a District, quickly.")
time.sleep(15)

browser.find_element_by_name(name="Command").click()

time.sleep(180)

def api_click(n):
    #n = row number
    return browser.find_element_by_xpath(f"//*[@id='myDataTable']/tbody/tr[{n}]/td[6]/a").click()

def prod_export():
    #download production data
    return browser.find_element_by_id("ButtonExportProdToExcel").click()

def set_page(p):
    browser.find_element_by_xpath(f"//*[@id='myDataTable_wrapper']/div[1]/div[4]/ul/li[{p}]/a").click()
    return 

def search_page():
    #return to search list
    return browser.find_element_by_xpath("//*[@id='navbar']/ul[2]/li/a").click()

def next_page():
    return browser.find_element_by_xpath("//*[@id='myDataTable_wrapper']/div[1]/div[4]/ul/li[10]/a").click()

time.sleep(7)

def page_scrape():
    for i in range(1,11):
        try:
            time.sleep(10)
            api_click(i)
            time.sleep(10)
            prod_export()
            time.sleep(8)
            search_page()
            time.sleep(15)
        except:
            time.sleep(15)
            search_page()
            i+=1
            continue
        i+=1
        if i == 11:
            time.sleep(10)
            next_page()
            time.sleep(10)
            page_scrape()
        
time.sleep(10)

page_scrape()




# for i in range(1,11):

#     try:

#         browser.find_element_by_xpath(f"//*[@id='myDataTable']/tbody/tr[{i}]/td[6]/a").click()

#         time.sleep(6)

#         browser.find_element_by_id("ButtonExportProdToExcel").click()

#         browser.find_element_by_xpath("//*[@id='navbar']/ul[2]/li/a").click()

#     except:
#         browser.find_element_by_xpath("//*[@id='navbar']/ul[2]/li/a").click()
#         i+=1
#         continue
 
#     i+=1

#     time.sleep(6)



#//*[@id="myDataTable"]/tbody/tr[2]/td[6]/a
#//*[@id="myDataTable"]/tbody/tr[10]/td[6]/a
#//*[@id="navbar"]/ul[2]/li/a
#//*[@id="select2-result-label-37"]
#//*[@id="select2-results-1"]/li[4]
#//*[@id="myDataTable"]/tbody/tr[1]/td[6]/a
#//*[@id="myDataTable"]/tbody/tr[11]/td[6]/a
#//*[@id="myDataTable_length"]/label/select


#//*[@id="myDataTable_wrapper"]/div[1]/div[4]/ul/li[3]/a

#//*[@id="myDataTable_wrapper"]/div[1]/div[4]/ul/li[4]/a

#//*[@id="myDataTable_wrapper"]/div[1]/div[4]/ul/li[4]/a

#//*[@id="myDataTable_wrapper"]/div[1]/div[4]/ul/li[10]/a
#//*[@id="myDataTable_paginate"]/ul/li[6]/a
#//*[@id="myDataTable_paginate"]/ul/li[6]/a
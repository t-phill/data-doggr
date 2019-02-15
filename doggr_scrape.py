from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium
import time

#Path to your ChromeDriver executable
browser = webdriver.Chrome('/Users/taylorphillips/galvanize/capstone/chromedriver')
#Navigation to DOGGR well search page
browser.get("https://secure.conservation.ca.gov/WellSearch")
print("Select a District, quickly.")
time.sleep(30)

#Clicks on Search
browser.find_element_by_name(name="Command").click()

#Time delay to select page number
print("Navigate to desired page, call function 'page_scrape()' in console.")

def api_click(n):
    #n = row number
    return browser.find_element_by_xpath(f"//*[@id='myDataTable']/tbody/tr[{n}]/td[6]/a").click()

def prod_export():
    #download production data
    return browser.find_element_by_id("ButtonExportProdToExcel").click()

#make functional later
# def set_page(p):
#     browser.find_element_by_xpath(f"//*[@id='myDataTable_wrapper']/div[1]/div[4]/ul/li[{p}]/a").click()
#     return 

def search_page():
    #return to search list
    return browser.find_element_by_xpath("//*[@id='navbar']/ul[2]/li/a").click()

def next_page():
    #navigate to next page
    return browser.find_element_by_xpath("//*[@id='myDataTable_wrapper']/div[1]/div[4]/ul/li[10]/a").click()


def page_scrape():
    #10 wells per page
    for i in range(1,11):
        try:
            time.sleep(10)
            api_click(i)
            time.sleep(10)
            prod_export()
            time.sleep(5)
            search_page()
            time.sleep(15)
        except:
            time.sleep(15)
            search_page()
            i+=1
            continue
        i += 1 
        if i == 11:
            time.sleep(10)
            next_page()
            time.sleep(10)
            page_scrape()
        else:
            continue
        

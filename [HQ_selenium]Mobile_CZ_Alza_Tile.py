#import requests
#import os
import datetime
import pandas as pd
#import difflib
from bs4 import BeautifulSoup
import sys

from selenium import webdriver
#from selenium.webdriver.common.alert import Alert


#drvpath = 'C:/WebDriver/'
drvpath = 'D:/Data_Analytics/Python/WebDriver/'
#drvpath = sys.argv[1]
#drvpath = 'C:/Users/j.h.jung/Documents/Automation Anywhere Files/Automation Anywhere/My Exes/C000/'

now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d")

d1 = {
    'Cntry' : "CZ",
    'Site' : "Alza",
    'Product' : "Mobile",
    'Page' : "https://www.alza.cz/mobily/18843445.htm",
    'Type' : "Tile",
    'Currency' : "CZK",
    #'Path' : ,  
    'Path' : "D:/Data_Analytics/WebScrapper/Result/",
    #'Path' : sys.argv[2],
    'Name_Class' : "name browsinglink",
    'Price_ID' : "boxes",
    'Price_Class' : "c2"
    }


#Selenium Option ####
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR") # 한국어!
options.add_argument("ignore-certificate-errors")
options.add_argument("ignore-ssl-errors")



driver = webdriver.Chrome(drvpath + 'chromedriver', options=options)
#driver = webdriver.Chrome(drvpath + 'chromedriver')

driver.implicitly_wait(3)


driver.get(d1['Page'])
driver.implicitly_wait(3)


def get_data(class_name):
    data_text = []
    list_data = list(soup.find_all(class_= class_name))
    for x in list_data:
        text = x.get_text().lstrip().rstrip()
        if text.find(')') is not -1:
            last = text.find(')')
            text = text[:last+1]
        if text != "":
            data_text.append(text)
    return data_text


def get_data2(id_name, class_name):
    data_text = []
    data1 = soup.find(id = id_name)
    list_data = list(data1.find_all(class_= class_name))
    for x in list_data:
        data_text.append(x.get_text().replace('\xa0', '').replace(',-', ''))
    return data_text


def replace_iphone(brand):
    if brand == "iPhone":
        brand_new = "Apple"
    else:
        brand_new = brand
    return brand_new


try:
       elem = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[2]/div/a/img')
       elem.click()
       driver.implicitly_wait(10)
except :  # NoSuchElementException:
       pass



try:
    page = driver.page_source
    
    
    soup = BeautifulSoup(page, 'html.parser')
    
    #print(soup)
    
    
    
    
    product_name = get_data(d1['Name_Class'])
    product_price = get_data2(d1['Price_ID'],d1['Price_Class'])
    
    d2 = {'Name':product_name, 'Price':product_price}
    df = pd.DataFrame(d2, columns=['Date', 'Product', 'Cntry', 'Site', 'Type', 'Rank', 'Brand', 'Model', 'Name', 'Price', 'Currency'])
    
    df['Date'] = today
    df['Site'] = d1['Site']
    df['Product'] = d1['Product']
    df['Type'] = d1['Type']
    df['Rank'] = df.index + 1
    df['Currency'] = d1['Currency']
    df['Cntry'] = d1['Cntry']
    df['Brand'] = df['Name'].str.split().str[0]
    
    
    df['Brand'] = df['Brand'].apply(replace_iphone)
    
    split_name = df['Name'].str.split()
    model = []
    for s in split_name:
        if len(s) > 3:
            new_name = s[1].replace(',','') + ' ' + s[2].replace(',','') + ' ' + s[3].replace(',','')
        else:
            new_name = s[1].replace(',','') + ' ' + s[2].replace(',','')
        model.append(new_name)
    
    cleaned_model = []
    for m in model:
        text = str(m)
        cleaned_text = text.encode("ascii", errors="ignore").decode()
        cleaned_model.append(cleaned_text)
    df['Model'] = cleaned_model
    
    if df.index.size > 25:
        df = df[:25]
    
    print(df)
    df.to_csv(d1['Path'] + d1['Product'] + "_" + d1['Cntry'] + "_" + d1['Site'] + "_" + d1['Type'] + "_" + today +".csv", sep=',', index = False)
    print("success")
except:
    print("fail")
    
    
driver.quit()
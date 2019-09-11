#from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
import time
import pandas as pd
import requests



now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d")



headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}


proxies = {'http' : 'http://168.219.61.252:8080',
           'https': 'https://168.219.61.252:8080'}



def get_name(class_name):
    data_name = []
    list_data = soup.find_all(class_=class_name)
    for x in list_data:
        prd_name = x.text.strip()
        data_name.append(prd_name)
    return data_name


def get_url(class_name):
    data_url = []
    list_data = soup.find_all(class_=class_name)
    for x in list_data:
        href = x.find('a').get('href')
        data_url.append(href)
    return data_url




baseurl = 'https://www.coupang.com'

url = 'https://www.coupang.com/np/categories/178456'



page = requests.get(url, proxies=proxies, headers=headers, verify=False)
page.status_code

soup = BeautifulSoup(page.content, 'html.parser')


prd_names = pd.DataFrame(get_name('name'))
prd_url = pd.DataFrame(get_url('baby-product renew-badge'))
prd_price = pd.DataFrame(get_name('price-value'))

result = pd.DataFrame(columns=['Date', 
                               'Product', 
                               'Cntry', 
                               'Site',
                               'Brand',
                               'Model', 
                               'Name', 
                               'Price',
                               'Currency'])

result[['Name']] = prd_names
result[['Price']] = prd_price
result[['Product']] = 'TV'
result['Date'] = today
result['Cntry'] = 'KOR'
result[['Site']] = baseurl + prd_url
result['Currency'] = 'KRW'
result['Brand'] = result['Name'].str.split().str[0]


detail_page = baseurl + prd_url[0]

page2 = requests.get(detail_page, proxies=proxies, headers=headers, verify=False)
page2.status_code

 

soup2 = BeautifulSoup(page2.content, 'html.parser')


model = soup2.find(class_='value').text
brand = soup2.find(class_='prod-brand-name').text

























list_data = soup.find_all(class_='baby-product renew-badge')

for x in list_data:
    href = x.find('a').get('href')
    print(href)
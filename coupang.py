from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
import time
import pandas as pd



now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d")



options = webdriver.ChromeOptions()

# headless 옵션 설정
#options.add_argument('headless')
#options.add_argument("no-sandbox")

# 브라우저 윈도우 사이즈
#options.add_argument('window-size=1920x10000')

# 사람처럼 보이게 하는 옵션들
options.add_argument("disable-gpu")   # 가속 사용 x
options.add_argument("lang=ko_KR")    # 가짜 플러그인 탑재
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')  # user-agent 이름 설정


drvpath = 'D:/Data_Analytics/Python/WebDriver/'


driver = webdriver.Chrome(drvpath + 'chromedriver', options = options)
driver.implicitly_wait(3)
driver.maximize_window()

baseurl = 'https://www.coupang.com'

url = 'https://www.coupang.com/np/categories/178456'

driver.get(url)


html = driver.page_source


soup = BeautifulSoup(html, 'html.parser')

prd_list = soup.find(class_='baby-product renew-badge')

prd_list

href = prd_list.find('a').get('href')

driver.get(baseurl + href)

html2 = driver.page_source

soup2 = BeautifulSoup(html2, 'html.parser')

model = soup2.find(class_='product-item__table').find('td').text
model
type(model)






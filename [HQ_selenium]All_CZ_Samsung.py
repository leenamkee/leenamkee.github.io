import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
import sys

### Path 수정 #####

#drvpath = 'C:/WebDriver/'
drvpath = 'D:/Data_Analytics/Python/WebDriver/'
#drvpath = sys.argv[1]
#drvpath = 'C:/Users/j.h.jung/Documents/Automation Anywhere Files/Automation Anywhere/My Exes/C000/'


#path = "C:/WebDriver/Samsung.com/cz/TV"
path = 'D:/Data_Analytics/WebScrapper/Result/'
#path = sys.argv[2]
#path = "C:/Users/j.h.jung/Documents/Automation Anywhere Files/UserInfo/C493/R1908099-001 Mobile_CZ/Output/"


### Date ######
now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d")


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
driver.implicitly_wait(3)

# Target URL (주석 해제)
url = ['http://www.samsung.com/cz/tvs/all-tvs/',
        'http://www.samsung.com/sk/tvs/all-tvs/',
        'http://www.samsung.com/cz/refrigerators/all-refrigerators/',
        'http://www.samsung.com/sk/refrigerators/all-refrigerators/',
        'http://www.samsung.com/cz/washing-machines/all-washing-machines/',
        'http://www.samsung.com/sk/washing-machines/all-washing-machines/',
        'http://www.samsung.com/cz/smartphones/all-smartphones/',
        'http://www.samsung.com/sk/smartphones/all-smartphones/']


def get_product(class_name):
    data_product = []
    list_data = list(soup.find_all(class_= class_name))
    for x in list_data:
        text = x.get_text().strip()
        data_product.append(text)
    return data_product


def get_price(class_name):
    data_price = []
    list_data = list(soup.find_all(class_= class_name))
    for x in list_data:
        text = x.get_text().lstrip('CENA').rstrip('Kč').replace(' ','').replace(',00€','') # ',00€' 제거
        data_price.append(text)
    return data_price


def get_model(class_name, tag_name):
    data_model = []
    list_data = list(soup.find_all(class_=class_name))
    for x in list_data:
        text = x.get(tag_name)
        data_model.append(text)
    return data_model


result_all = pd.DataFrame(columns=['Date', 
                                   'Product', 
                                   'Cntry', 
                                   'Site',
                                   'Brand',
                                   'Model', 
                                   'Name', 
                                   'Price',
                                   'Currency'])
#result_tmp = result_all.copy()

try:
    for u in url:
    
        driver.get(u)
        driver.implicitly_wait(100)
    
        #최초화면 Source
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
    
        # Item 갯수 구하기 에 따라 더보기 버튼 클릭 ##
        items = int(soup.find(class_='s-sort-number').get_text())
    
        # Item 갯수에 따라 더보기 버튼 클릭 ##
        for i in range(0,int(items/12)): #총페이지수 int((item/12)) + 1
            try:
                elem = driver.find_element_by_xpath("//*[@id='content']/div[4]/div[3]/div/a")
                #elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='content']/div[4]/div[3]/div/a")))
                #elem = driver.find_elements_by_css_selector('#content > div.shop-pf-card.product-card-group__list--mode-list > div.shop-pf-card__nav > div > a')
                elem.click()
                driver.implicitly_wait(100)
            except :  # NoSuchElementException:
                pass        
            
        #전체 상품 대상 화면 Source
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
    
        # Model Text
        prd_text = pd.DataFrame({'Name' : get_product('s-txt-title')})                   
        # Model
        prd_model = pd.DataFrame({'Model' : get_model('s-txt-title', 'data-omni')})
        # Price (재고가 있는 경우만 조회됨)
        prd_price = pd.DataFrame({'Price' : get_price('cm-shop-card__price')})
        
        result_tmp = pd.DataFrame(columns=['Date', 
                                           'Product', 
                                           'Cntry', 
                                           'Site',
                                           'Brand',
                                           'Model', 
                                           'Name', 
                                           'Price',
                                           'Currency']) ######## tmp 초기화 
    
        result_tmp[['Model']] = prd_model
        result_tmp[['Name']] = prd_text
        result_tmp[['Price']] = prd_price
    
        result_tmp['Date'] = today
        result_tmp['Site'] = 'Samsung.com'
        result_tmp['Brand'] = 'Samsung'
        if '/sk/' in u:
            result_tmp['Currency'] = 'EUR'
            result_tmp['Cntry'] = 'SK'
        else:
            result_tmp['Currency'] = 'CZK'
            result_tmp['Cntry'] = 'CZ'
            
        if '/tvs/' in u:
            result_tmp['Product'] = 'TV'
        elif '/refrigerators/' in u:
            result_tmp['Product'] = 'Refrigerator'
        elif '/washing-machines/' in u:
            result_tmp['Product'] = 'WM'
        elif '/smartphones/' in u:
            result_tmp['Product'] = 'Mobile'
        
        result_tmp = result_tmp[:(items)]    
        result_all = result_all.append(result_tmp) ###### result_all.append(result_tmp)
        
    print(result_all)
    
    result_all.to_csv(path+'All_Samsung.com'+"_"+today+'.csv', sep=',', index = False)
    #result_all.to_excel(path+'All_Samsung.com'+"_"+today+'.csv', sep=',', index = False)
    print("success")
except:
    print("fail")

driver.quit()

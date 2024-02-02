from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime


options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
options.add_argument('user_agent=' + user_agent)
options.add_argument('lang=ko_KR')
#options.add_argument('headless') #메모리에만 띄우고 유저에게 보이는 창은 안띄운다.
#options.add_argument('window-size=1920X1080') #사이즈를 정해줄 수 있다. 방은형 페이지의 경우 xpath가 바뀔수 있으니 창크기 고정해준다.

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

start_url = 'https://m.kinolights.com/discover/explore'
button_movie_tv_xpath = '//*[@id="contents"]/section/div[3]/div/div/div[3]/button'
button_movie_xpath = '//*[@id="contents"]/section/div[4]/div[2]/div[1]/div[3]/div[2]/div[2]/div/button[1]'
button_ok_xpath = '//*[@id="applyFilterButton"]'
driver.get(start_url)
time.sleep(0.5)
button_movie_tv = driver.find_element(By.XPATH, button_movie_tv_xpath)
driver.execute_script('arguments[0].click();', button_movie_tv) #자바스크립트로 되있어서 이런식으로 해줘야 한다...
time.sleep(1)
button_movie = driver.find_element(By.XPATH, button_movie_xpath)
driver.execute_script('arguments[0].click();', button_movie)
time.sleep(1)
button_ok = driver.find_element(By.XPATH, button_ok_xpath)
driver.execute_script('arguments[0].click();', button_ok)
time.sleep(2)

cnt = 15

for i in range(cnt):
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(0.8)

movie_titles = []
list_review_url = []
review_list = []

items = driver.find_elements(By.CLASS_NAME, 'MovieItem')
for item in items[450:500]:
    item = item.find_element(By.TAG_NAME, 'a')
    link = f"{item.get_attribute('href')}/reviews"
    title = item.get_attribute('title')
    movie_titles.append(title)
    list_review_url.append(link)
    print(title, link)

for url in list_review_url:
    driver.get(url)
    time.sleep(1)
    try:
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div[3]/button').click() #광고 오늘은 재생 안함
        time.sleep(1)
    except:
        pass

    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1.5)

    reviews = driver.find_elements(By.CLASS_NAME, 'review-item')
    print(len(reviews), reviews)
    reviews_url = []
    for review in reviews[:31]:
        reviews_url.append(review.find_element(By.CLASS_NAME, 'review-content-link').get_attribute('href'))
    text = ''
    print(reviews_url)
    for review_url in reviews_url:
        try:
            driver.get(review_url)
            time.sleep(1)
            text = text + ' ' + driver.find_element(By.CLASS_NAME, 'review-content-wrap').text
            print(driver.find_element(By.CLASS_NAME, 'review-content-wrap').text)
        except:
            print('스포일러')
    driver.close()

    print(text)
    review_list.append(text)

df = pd.DataFrame({'titles': movie_titles[450:500], 'review': review_list})
print(df.head())
print(df['titles'].value_counts())
df.to_csv('./data[450:500]_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)
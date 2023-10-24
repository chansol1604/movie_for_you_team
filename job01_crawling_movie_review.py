from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
import time



options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경

date = 1301
url = 'https://movie.daum.net/ranking/boxoffice/monthly?date=20'


df_movie = pd.DataFrame()

titles = []
reviews = []
crawled_titles = []

for i in range(24):
    section_url = url+ str(date)
    driver.get(section_url)
    time.sleep(0.5)

    for j in range(1,31):
        try:
            movie = driver.find_element('xpath','//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(j)).click()
            review_page = driver.find_element('xpath', '//*[@id="mainContent"]/div/div[2]/div[1]/ul/li[4]').click()
            driver.refresh()
            for _ in range(5):
                try:
                    time.sleep(1)
                    click = driver.find_element('xpath', '//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button').click()
                except:
                    print('페이지가 없습니다.')
                    break
            for l in range(1, 161):
                try:
                    review = driver.find_element('xpath', '/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[{}]/div/p'.format(l)).text
                    review = re.compile('[^가-힣]').sub(' ', review)
                    title = driver.find_element('xpath','//*[@id="mainContent"]/div/div[1]/div[2]/div[1]/h3/span[1]').text
                    print('{}. {} : {}'.format(l,title, review))
                    if title in crawled_titles:
                        continue
                    crawled_titles.append(title)
                    titles.append(title)
                    reviews.append(review)
                except:
                    print("리뷰가 없습니다.")
            driver.back()
            driver.back()
        except:
            print('페이지가 없습니다.')
    df_movie = pd.DataFrame({'title':titles, 'review':reviews})
    df_movie.to_csv('./crawling_data/crawling_data_{}_{}.csv'.format(int(date/100),date%100), index = False)
    titles = []
    reviews = []
    date += 1
    if date % 100 == 13:
        date = date + 100 - 12







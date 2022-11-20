from bs4 import BeautifulSoup
from selenium import webdriver
# import chromedriver_binary
import pandas as pd
import os
import datetime as dt

base_url = 'https://prtimes.jp'
driver = webdriver.Chrome()
search_comps = ['インフォマート', 'マネーフォワード', 'LayerX', 'TOKIUM']
# TODO 検索ワードを増やす
driver.get("https://prtimes.jp/main/action.php?run=html&page=searchkey&search_word=請求書")

content = driver.page_source
soup = BeautifulSoup(content, "html.parser")

save_dir = 'track_pdfs'
if save_dir not in os.listdir("./"):
    os.mkdir(save_dir)
file_names = []

news_list = []

for element in soup.findAll(attrs={"class": "list-article"}):
    title = element.find(attrs={"class": "list-article__title"}).string.strip()
    time_str = element.find(attrs={"class": "list-article__time"}).string.strip()
    time = dt.datetime.strptime(time_str, "%Y年%m月%d日 %H時%M分")
    comp_name = element.find(attrs={"class": "list-article__company-name--dummy"}).string.strip()
    if not [s for s in search_comps if s in comp_name]:
        continue
    if time < dt.datetime.now() - dt.timedelta(days = 3):
        break
    link = element.find(attrs={"class": "list-article__link"})["href"].strip()
    
    news = [title, comp_name, time, link]
    news_list.append(news)

print(news_list)

driver.quit




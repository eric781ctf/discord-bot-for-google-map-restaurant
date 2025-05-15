from configs.config import CONFIGURATION
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json
import emoji
import re
import os
from serpapi import GoogleSearch
from google_maps import parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time

 
class SerpAPICrawler:
    def __init__(self, url):
        self.headers = CONFIGURATION.HEADERS
        self.store_url = url
        self.comment_url = "https://www.google.com.tw/maps/rpc/listugcposts"
        
        
    def get_store_id(self):
        pattern = r'0x.{16}:0x[^!]+'
        match = re.search(pattern, self.store_url) 
        if not match:
            raise ValueError(f"[ERROR] 無法擷取 store_id，請確認網址是否正確：{self.store_url}")
        store_id = match.group()
        print(f'Get store id: {store_id}')
        
        return store_id

    def get_comment(self, store_id):
        '''
        sorted_by 參數對應：
        1 - 最相關 (Most Relevant)
        2 - 最新 (Newest)
        3 - 評分最高 (Highest Rating)
        4 - 評分最低 (Lowest Rating)
        
        每個 page 會有10筆資料，除非評論數未達10筆

        '''
        params = {
            "engine": "google_maps_reviews",
            "data_id": store_id,
            "hl": "fr",
            "api_key": os.getenv("SURP_API_KEY"),
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        print(results)
        reviews = results["reviews"] # its a list
        
        All_keywords_matched = []
        All_comment_matched = []
        for review in reviews:
            if 'extracted_snippet' in review:
                comment = emoji.demojize(review['extracted_snippet']['original'])
            else:
                comment = emoji.demojize(review['snippet'])
            matched_keywords = parse.check_keywords(comment, CONFIGURATION.KeyWordsList)
            if len(matched_keywords)>0:
                data = {'發布日期':review['iso_date_of_last_edit'],'評論':comment}
                All_comment_matched.append(data)
                for matched in matched_keywords:
                    if matched not in All_keywords_matched:
                        All_keywords_matched.append(matched)

        return All_comment_matched, All_keywords_matched
    
class SeleniumCrawler:
    def __init__(self, url):
        self.headers = CONFIGURATION.HEADERS
        self.store_url = url

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # 無頭模式
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(service=Service(), options=options)


    


# 輸入目標商家名稱
target = "星巴克 台北車站"

# 建立瀏覽器
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(), options=options)

# 開啟 Google Maps 並搜尋
driver.get("https://www.google.com/maps")
time.sleep(3)

# 搜尋商家
search_box = driver.find_element(By.ID, "searchboxinput")
search_box.send_keys(target)
search_box.send_keys(Keys.ENTER)
time.sleep(5)

# 點擊評論按鈕（需要視商家頁面結構調整）
try:
    review_button = driver.find_element(By.CSS_SELECTOR, 'button[jsaction="pane.reviewChart.moreReviews"]')
    review_button.click()
    time.sleep(5)
except:
    print("找不到評論按鈕")

# 滾動評論區塊
scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="評論"]')
for _ in range(10):  # 滾動10次
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
    time.sleep(2)

# 抓取評論內容
reviews = driver.find_elements(By.CSS_SELECTOR, 'div[jscontroller="e6Mltc"]')
for review in reviews:
    try:
        author = review.find_element(By.CLASS_NAME, 'd4r55').text
        rating = review.find_element(By.CSS_SELECTOR, 'span[jsname="bN97Pc"]').get_attribute("aria-label")
        content = review.find_element(By.CLASS_NAME, 'wiI7pd').text
        print(f"作者: {author}\n評分: {rating}\n評論內容: {content}\n{'='*40}")
    except:
        continue

driver.quit()

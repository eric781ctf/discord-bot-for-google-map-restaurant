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
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")  # 無頭模式
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(service=Service(), options=self.options)

    def work(self):
        # 開啟 URL 並搜尋
        self.driver.get(self.store_url)
        time.sleep(1.5)

        # 點擊評論按鈕（需要視商家頁面結構調整）
        try:
            review_tab = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label*="的評論"]')
            review_tab.click()
        except:
            print("找不到評論按鈕")

        # 滾動評論區塊
        scrollable_div = self.driver.find_element(By.CSS_SELECTOR, CONFIGURATION.SCROLLABLE_DIV_ID)
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        for _ in range(CONFIGURATION.ScrollPage):  # 最多滾 10 次（可視情況調整）
            self.driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight);', scrollable_div)
            time.sleep(2)  # 等待評論載入
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
            
            all_reviews = self.driver.find_elements(By.CSS_SELECTOR, CONFIGURATION.BLOCKS_DIC_ID)
            print(f"目前共有 {len(all_reviews)} 筆評論載入")
            if new_height == last_height:
                break
            last_height = new_height

        # 抓取評論內容
        review_blocks = self.driver.find_elements(By.CSS_SELECTOR, CONFIGURATION.BLOCKS_DIC_ID)

        # 擷取評論內容
        all_reviews = []
        
        for block in review_blocks:
            try:
                # 嘗試點擊「全文」按鈕
                more_button = block.find_element(By.CSS_SELECTOR, CONFIGURATION.MORE_BUTTON_ID)
                if more_button.is_displayed():
                    self.driver.execute_script("arguments[0].click();", more_button)
                    time.sleep(0.2)  # 給點時間讓文字展開

                # 抓取展開後的評論內容
                content = block.find_element(By.CSS_SELECTOR, CONFIGURATION.BLOCK_SPAN_ID).text
                all_reviews.append(content)
            except Exception as e:
                print(f"⚠️ 抓取評論失敗: {e}")
                continue
        self.driver.quit()

        All_keywords_matched = []
        All_comment_matched = []
        for review in all_reviews:
            # comment = emoji.demojize(review)
            comment = review
            matched_keywords = parse.check_keywords(comment, CONFIGURATION.KeyWordsList)
            if len(matched_keywords)>0:
                All_comment_matched.append(comment)
                for matched in matched_keywords:
                    if matched not in All_keywords_matched:
                        All_keywords_matched.append(matched)
        print(f"評論數量: {len(all_reviews)}")
        return All_comment_matched, All_keywords_matched
        



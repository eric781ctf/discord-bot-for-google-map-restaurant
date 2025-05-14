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

 
class GoogleMapCrawler:
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
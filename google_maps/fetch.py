import requests
from bs4 import BeautifulSoup
from configs.config import CONFIGURATION

def get_reviews(google_map_url: str):
    # 模擬：實際上你可能要處理 redirect 或 query string
    response = requests.get(google_map_url, headers=CONFIGURATION.HEADERS)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 假設評論都在某些 tag 中
    reviews = [r.text for r in soup.find_all("span") if "星" in r.text]
    return reviews

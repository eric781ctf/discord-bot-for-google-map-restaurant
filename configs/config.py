import json 
import os

class CONFIGURATION:
    HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Referer": "https://www.google.com"
        }
    
    with open(os.path.join(os.path.dirname(__file__), 'keywords.json'), encoding='utf-8') as f:
            KEYWORDS = json.load(f)
    KeyWordsList = KEYWORDS
    DC_API_KEY = os.getenv("DC_API_KEY")
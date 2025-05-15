import json 
import os

class CONFIGURATION:
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
        ),
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document"
    }
    
    with open(os.path.join(os.path.dirname(__file__), 'keywords.json'), encoding='utf-8') as f:
            KEYWORDS = json.load(f)
    KeyWordsList = KEYWORDS
    DC_API_KEY = os.getenv("DC_API_KEY")
    ScrollPage = 10
    SCROLLABLE_DIV_ID = 'div.m6QErb.DxyBCb.kA9KIf.dS8AEf'
    BLOCKS_DIC_ID = 'div.jftiEf'
    BLOCK_SPAN_ID = 'span.wiI7pd'
    MORE_BUTTON_ID = 'button.w8nwRe'
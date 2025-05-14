import json
from collections import Counter
import re

with open("config/keywords.json", "r", encoding="utf-8") as f:
    KEYWORDS = json.load(f)

def analyze_reviews(reviews):
    counter = Counter()
    for review in reviews:
        for keyword in KEYWORDS:
            if re.search(keyword, review):
                counter[keyword] += 1
    return counter

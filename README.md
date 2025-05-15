# discord-bot-for-google-map-restaurant
[中文說明](/documents/README_zh_TW.md)

## 📌 Project Overview

This is a Discord Bot designed to analyze whether a business linked through Google Maps offers promotions such as "check-in for freebies" or "5-star reviews for gifts." Users can simply enter the command `!check {google_map_url}` to perform the check.

---

## 🚀 Features

- ✅ Accepts Google Maps business URLs submitted by users
- ✅ Automatically extracts reviews from the specified business
- ✅ Analyzes whether reviews contain promotional keywords (e.g., "5-star review gift", "comment bonus", "check-in bonus")
- ✅ Returns the analysis result in the Discord channel

---

## 🛠️ Installation & Usage

### 1. Requirements
- Python 3.11 or later
- Required packages (see `requirements.txt`)

### 2. Installation Steps
1. Clone the project:
```bash
git clone https://github.com/your-repo/discod-bot-for-google-map-restaurant.git
cd discod-bot-for-google-map-restaurant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Note: This project uses Selenium headless mode to scrape reviews. Make sure to download the ChromeDriver!

3. Set environment variables:
```python
DC_BOT_TOKEN=your_bot_token
```

4. Start the bot:
```bash
python main.py
```

## 📋 Command Description
```bash
!check {google_map_url}
```
- Function: Analyzes the Google Maps business link and checks if any reviews contain promotional keywords.
- Example:
```bash
!check https://www.google.com/maps/place/...
```
- Response:
  - If keywords are found:
```
✅ 評論中找到了以下關鍵字：
五星好評送 / 打卡送
以下僅列出5則留言供參考
發布日期:2023-10-01
評論:五星好評送贈品，超棒的服務！
====================
發布日期:2023-09-28
評論:打卡送甜點，值得推薦！
```
  - If no keywords are found:
```
❌ 評論中沒有找到相關關鍵字。
```

## 📂 Project Structure
```
.env
.gitignore
main.py
README.md
requirements.txt
bot/
    __init__.py
    commands.py
configs/
    config.py
    keywords.json
google_maps/
    __init__.py
    crawler.py
    parse.py
```

## 🔑 Keyword Configuration
Promotional keywords are stored in configs/keywords.json. You can modify or add new keywords as needed. Example:

```json
[
    "五星",
    "五星好評送",
    "評論送",
    "打卡送",
    "贈送",
    "活動送"
]
```

## 🛡️ Notes
1. Do not upload your .env file to any public version control system to ensure the security of sensitive information.






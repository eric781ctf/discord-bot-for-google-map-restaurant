# discod-bot-for-google-map-restaurant

## 📌 專案簡介

這是一個 Discord Bot，用於分析 Google 地圖連結所指向的商家，是否存在「打卡送東西」、「五星好評送贈品」等優惠活動。使用者透過簡單指令 `!check {google_map_url}` 即可查詢。

---

## 🚀 功能特色

- ✅ 支援使用者提交 Google Maps 商家連結
- ✅ 自動擷取該商家的評論內容
- ✅ 分析評論是否包含優惠關鍵字（如：五星好評送、評論送、打卡送等）
- ✅ 回傳分析結果至 Discord 頻道

---

## 🛠️ 安裝與使用

### 1. 環境需求
- Python 3.11 或以上版本
- 必要套件（詳見 `requirements.txt`）

### 2. 安裝步驟
1. clone 此專案：
```bash
git clone https://github.com/your-repo/discod-bot-for-google-map-restaurant.git
cd discod-bot-for-google-map-restaurant
```

2. 安裝必要套件：
```bash
pip install -r requirements.txt
```

3. 設定環境變數：
```python
DC_BOT_TOKEN=your_bot_token
SURP_API_KEY=your_serp_api_key
```

4. 啟動 Bot：
```bash
python main.py
```

## 📋 指令說明
```bash
!check {google_map_url}
```
- 功能：分析指定的 Google 地圖商家連結，檢查評論中是否包含優惠關鍵字。
- 範例：
```bash
!check https://www.google.com/maps/place/...
```
- 回應：
  - 若找到關鍵字：
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
  - 若未找到關鍵字：
```
❌ 評論中沒有找到相關關鍵字。
```

## 📂 專案結構
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

## 🔑 關鍵字設定
關鍵字儲存在 configs/keywords.json 中，您可以根據需求新增或修改關鍵字。例如：

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

## 🛡️ 注意事項
1. 請勿將 .env 檔案上傳至公開的版本控制系統，確保敏感資訊的安全。
2. 確保 SURP_API_KEY 有效，否則無法正確爬取 Google 地圖評論。






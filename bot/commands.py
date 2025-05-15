from discord.ext import commands
from google_maps import crawler, parse
from configs.config import CONFIGURATION
import asyncio
import uuid

active_sessions = set()
def setup_commands(bot: commands.Bot):
    @bot.command(name="help")
    async def help_message(ctx):
        help_text = (
            "## 🤖 Discord Google 地圖評論查詢機器人\n"
            "這是一個 Discord Bot，能協助你快速查詢 Google 地圖商家的評論內容。\n"
            "你可以用這個 Bot 來檢查特定地點的評論中，是否有出現特定關鍵字（目前主要偵測洗評論相關字詞）。\n"
            "\n"
            "## 📝 使用說明：\n"
            "1. 輸入 `!check <Google 地圖連結>` 來查詢評論。\n"
            "2. 請確保提供的是有效的 Google 地圖商家連結（不要貼搜尋結果頁的連結）。\n"
            "3. 查詢完成後，會顯示找到的關鍵字與相關評論。\n"
            "\n"
            "## 🔍 分析與結果：\n"
            "- 為了提升效率，目前僅擷取部分評論進行分析。\n"
            "- 會顯示總評論數與符合條件的評論數。\n"
            "- 若有找到符合條件的評論，會列出前** 五則 **內容供參考。\n"
            "\n"
            "## 💡 其他說明：\n"
            "1. 目前 Bot 僅偵測預設關鍵字，未來將持續擴充功能。\n"
            "2. 有任何建議或問題，歡迎聯繫開發者，或至 [GitHub](https://github.com/eric781ctf/discord-bot-for-google-map-restaurant)開 issue。\n"
        )
        await ctx.send(help_text)

    @bot.command(name="check")
    async def check_google_map(ctx, url: str):
        user_key = (ctx.author.id, url)
        if user_key in active_sessions:
            await ctx.send("⚠️ 正在查詢中，請勿重複發送指令")
            return
        try:
            active_sessions.add(user_key)
            session_id = uuid.uuid4()
            print(f"🔁 New check_google_map session: {session_id}")
            if not url or ("https://www.google.com.tw/" not in url and "https://maps.app.goo.gl" not in url):
                await ctx.send("❗ 請提供 Google 地圖的連結，例如：\n`!check https://www.google.com/maps/place/...`")
                return
            await ctx.send("🔍 正在查詢評論，請稍候...")
            gmc = crawler.SeleniumCrawler(url)
            All_reviews = None
            All_comment_matched = None
            All_keywords_matched = None
            All_reviews, All_comment_matched, All_keywords_matched = await asyncio.to_thread(lambda: gmc.work())
            print('All_comment_matched:',All_comment_matched)
            print('All_keywords_matched: ',All_keywords_matched)
            
            if len(All_comment_matched)>0 and len(All_keywords_matched)>0:
                merge_text = f"✅ 於{len(All_comment_matched)} / {len(All_reviews)}評論中找到了以下關鍵字：\n" + " / ".join(All_keywords_matched)+"\n"
                await ctx.send(merge_text)
                if len(All_comment_matched)>5:
                    All_comment_matched = All_comment_matched[:5]
                merge_text = ""
                for i, comment in enumerate(All_comment_matched):
                    merge_text += f"評論:{comment}"
                    if i != len(All_comment_matched) - 1:
                        merge_text += f"\n====================\n"
                await ctx.send(merge_text)
            elif len(All_comment_matched)==0 and len(All_keywords_matched)==0:
                print('評論中沒有找到相關關鍵字')
                await ctx.send(f"❌ 抓取了{len(All_comment_matched)}筆評論，沒有找到相關關鍵字。")
        finally:
            active_sessions.discard(user_key)
            print(f"🔚 清除 active_sessions: {user_key}")

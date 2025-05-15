from discord.ext import commands
from google_maps import crawler, parse
from configs.config import CONFIGURATION
import asyncio
import uuid

active_sessions = set()
def setup_commands(bot: commands.Bot):
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
            All_comment_matched = None
            All_keywords_matched = None
            All_comment_matched, All_keywords_matched = await asyncio.to_thread(lambda: gmc.work())
            print('All_comment_matched:',All_comment_matched)
            print('All_keywords_matched: ',All_keywords_matched)
            
            if len(All_comment_matched)>0 and len(All_keywords_matched)>0:
                await ctx.send("✅ 評論中找到了以下關鍵字：\n" + " / ".join(All_keywords_matched)+"\n以下僅列出5則留言供參考")
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
                await ctx.send("❌ 評論中沒有找到相關關鍵字。")
        finally:
            active_sessions.discard(user_key)
            print(f"🔚 清除 active_sessions: {user_key}")

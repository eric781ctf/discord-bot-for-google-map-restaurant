from discord.ext import commands
from google_maps import crawler, parse
from configs.config import CONFIGURATION

def setup_commands(bot: commands.Bot):
    @bot.command(name="check")
    async def check_google_map(ctx, url: str):
        if not url or "https://www.google.com.tw/maps/place" not in url:
            await ctx.send("❗ 請提供 Google 地圖的連結，例如：\n`!check https://www.google.com/maps/place/...`")
            return
        gmc = crawler.GoogleMapCrawler(url)
        All_comment_matched, All_keywords_matched = gmc.get_comment(gmc.get_store_id())
        
        if len(All_comment_matched)>0 and len(All_keywords_matched)>0:
            await ctx.send("✅ 評論中找到了以下關鍵字：\n" + " / ".join(matched)+"\n以下僅列出5則留言供參考")
            if len(All_comment_matched)>5:
                All_comment_matched = All_comment_matched[:5]
            merge_text = ""
            for i, comment in enumerate(All_comment_matched):
                merge_text += f"發布日期:{comment['發布日期']}\n評論:{comment['評論']}"
                if i != len(All_comment_matched) - 1:
                    merge_text += f"\n====================\n"
        else:
            await ctx.send("❌ 評論中沒有找到相關關鍵字。")

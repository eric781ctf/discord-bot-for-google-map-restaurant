from discord.ext import commands
from bot.google_map_parser import extract_place_info
from bot.keyword_analyzer import analyze_reviews

def setup_commands(bot):
    @bot.command(name="check")
    async def check(ctx, url: str):
        await ctx.send("🔍 正在分析該商家的評論，請稍候...")

        place_name, reviews = extract_place_info(url)
        result = analyze_reviews(reviews)

        msg = f"🎯 商家名稱：{place_name}\n\n"
        msg += f"共分析 {len(reviews)} 則評論，其中發現：\n"
        for keyword, count in result.items():
            msg += f"- {count} 則評論提到「{keyword}」\n"

        if result:
            msg += "\n✅ 該商家可能有優惠活動，建議進店前可確認"
        else:
            msg += "\n❌ 未發現與活動相關的評論"

        await ctx.send(msg)

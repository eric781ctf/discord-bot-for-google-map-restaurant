from discord.ext import commands
from google_maps import fetch, parse
from config import keywords

bot = commands.Bot(command_prefix="!")

@bot.command(name="check")
async def check_google_map(ctx, url: str):
    reviews = fetch.get_reviews(url)
    matched = parse.check_keywords(reviews, keywords.KEYWORDS)
    
    if matched:
        await ctx.send(f"✅ 找到活動相關評論：\n{matched}")
    else:
        await ctx.send("❌ 沒有找到相關活動評論。")

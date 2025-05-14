import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from bot.commands import setup_commands

load_dotenv()
print('1')
TOKEN = os.getenv("DC_BOT_TOKEN")
print('2')
intents = discord.Intents.default()
print('3')
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
print('4')

setup_commands(bot)
print('5')

bot.run(TOKEN)

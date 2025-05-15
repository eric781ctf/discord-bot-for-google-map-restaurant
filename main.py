import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from bot.commands import setup_commands
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug("Starting the bot...")

load_dotenv()
TOKEN = os.getenv("DC_BOT_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
setup_commands(bot)
bot.run(TOKEN)

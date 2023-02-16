from dotenv import load_dotenv
from os import getenv
from discord.ext import commands
import discord

load_dotenv()
TOKEN = getenv('TOKEN')
PREFIX = getenv('prefix')
intents = discord.Intents.all()
description = "Hi pupaling how can I help you?"

bot = commands.Bot(command_prefix=PREFIX, description=description, intents=intents)

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(description="I respond with Hello")
async def hello(ctx):
    await ctx.send("Hello!")



bot.run(TOKEN)
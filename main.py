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

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=limit)

@bot.event
async def on_ready():
    print(f"Alright logged in as {bot.user}\n---------------------------------------")

bot.run(TOKEN)
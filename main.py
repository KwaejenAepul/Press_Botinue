import asyncio
from os import getenv, listdir

import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils.config import prefix

_ = load_dotenv()
TOKEN = getenv("TOKEN", "")
intents = discord.Intents.all()

bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)


@bot.event
async def on_ready():
    print(f"Alright logged in as {bot.user}\n---------------------------------------")


async def load():
    for file in listdir("./cogs"):
        if file.endswith(".py"):
            print(f"loading: {file}")
            await bot.load_extension(f"cogs.{file[:-3]}")


async def main():
    await load()
    await bot.start(TOKEN)


asyncio.run(main())

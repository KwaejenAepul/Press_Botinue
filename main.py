from dotenv import load_dotenv
from os import getenv
from discord.ext import commands
import discord
import sqlite3

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
    conn = sqlite3.connect('press.db')
    c = conn.cursor()
    t = (str(message.author.id),)
    c.execute("UPDATE points SET pupapoints = pupapoints + 1 WHERE member=?", t)
    conn.commit()
    conn.close()
    

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=limit)

@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member = None):
    await member.ban()


#DATABASE SHIT
@bot.command()
@commands.has_permissions(ban_members=True)
async def init_database(ctx):
    conn = sqlite3.connect('press.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS points (member UNIQUE , pupapoints INT)''')
    for i in ctx.guild.members:
        if i.id == bot.user.id:
            pass
        try:
            c.execute("INSERT INTO points VALUES(?,?)", (str(i.id), 0))
            conn.commit()
        except:
            print(f"couldn't add {i.id}")
    conn.close()

@bot.event
async def on_ready():
    print(f"Alright logged in as {bot.user}\n---------------------------------------")

bot.run(TOKEN)
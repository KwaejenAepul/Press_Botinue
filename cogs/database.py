from discord.ext import commands
import discord
import sqlite3

class database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def init_db(self, ctx):
        conn = sqlite3.connect('press.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS points (member UNIQUE , pupapoints INT, warnings INT, timeouts INT, lasttimeout TEXT)''')
        for i in ctx.guild.members:
            try:
                member = (str(i.id), 0, 0, 0,"")
                c.execute("INSERT INTO points VALUES(?,?,?,?,?)", member)
                conn.commit()
            except:
                pass
        conn.close()
        await ctx.send("member db created")
    
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def init_warndb(self, ctx):
        conn = sqlite3.connect('press.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS warnings (member TEXT, reason TEXT, date TEXT)''')
        conn.commit()
        conn.close()
        await ctx.send("warning db created")

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def init_worddb(self, ctx):
        conn = sqlite3.connect('press.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS words (word UNIQUE)''')
        conn.commit()
        conn.close()
        await ctx.send("word table created")

    @commands.command()
    @commands.has_guild_permissions(ban_members = True)
    async def init_timeouttracker(self,ctx):
        conn = sqlite3.connect('press.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS timeouts (member TEXT, date TEXT)''')
        conn.commit()
        conn.close()
        await ctx.send("timeout tracker created")
        
async def setup(bot):
    await bot.add_cog(database(bot))
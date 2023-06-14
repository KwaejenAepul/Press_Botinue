from discord.ext import commands
import sqlite3


class database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def init_db(self, ctx):
        conn = sqlite3.connect("press.db")
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS points (member UNIQUE , warnings INT, totalwarnings INT, timeouts INT, lasttimeout TEXT)"""
        )
        await ctx.send("member db created")
        c.execute(
            """CREATE TABLE IF NOT EXISTS warnings (member TEXT, reason TEXT, date TEXT)"""
        )
        await ctx.send("warning db created")
        c.execute("""CREATE TABLE IF NOT EXISTS words (word UNIQUE)""")
        await ctx.send("word table created")
        c.execute("""CREATE TABLE IF NOT EXISTS timeouts (member TEXT, date TEXT)""")
        conn.commit()
        conn.close()
        await ctx.send("timeout tracker created")
        
async def setup(bot):
    await bot.add_cog(database(bot))

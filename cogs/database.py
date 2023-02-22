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
        c.execute('''CREATE TABLE IF NOT EXISTS points (member UNIQUE , pupapoints INT, warnings INT, timeouts INT)''')
        for i in ctx.guild.members:
            try:
                member = (str(i.id), 0, 0, 0)
                c.execute("INSERT INTO points VALUES(?,?,?,?)", member)
                conn.commit()
            except:
                pass
        conn.close()
    
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def init_warndb(self, ctx):
        conn = sqlite3.connect('press.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS warnings (member TEXT, reason TEXT, date TEXT)''')
        conn.commit()
        conn.close()
        
async def setup(bot):
    await bot.add_cog(database(bot))
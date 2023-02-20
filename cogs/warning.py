from discord.ext import commands
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
import discord
import sqlite3

#read out all warnings from specific member
#remove warning entry after X days
#remove warnings
#get warnings of specific member

class warning(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warn_max = 3
        self.timeout_length = 300
    
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def init_warndb(self, ctx):
        conn = sqlite3.connect('press.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS warnings (member TEXT, reason TEXT, date TEXT)''')
        conn.commit()
        conn.close()
        
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def warn(self, ctx, member: discord.Member = None):
        t = (str(member.id),)
        conn = sqlite3.connect("press.db")
        c = conn.cursor()
        c.execute("UPDATE points SET warnings = warnings + 1 WHERE member=?", t)
        conn.commit()
        contents = ctx.message.content.split()
        reason = " ".join(str(i) for i in contents[2:])
        date = str(datetime.today() + relativedelta(days=1)).split()
        warn_entry = (str(member.id), reason, date[0])
        c.execute("INSERT INTO warnings VALUES(?,?,?)", warn_entry)
        conn.commit()
        c.execute("SELECT warnings FROM points WHERE member=?", t)
        value = c.fetchone()
        await ctx.send(f"{member.name} has been warned!")
        if value[0] == self.warn_max:
            c.execute("UPDATE points SET warnings = 0, timeouts = timeouts + 1 WHERE member=?", t)
            conn.commit()
            await member.timeout(timedelta(seconds=self.timeout_length))
            await ctx.send(f"{member.name} got {self.warn_max} warnings and is in time out")
        conn.close()

async def setup(bot):
    await bot.add_cog(warning(bot))
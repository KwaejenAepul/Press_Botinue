from discord.ext import commands, tasks
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
import discord
import sqlite3

#read out all warnings from specific member
#remove warnings

class warning(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warn_max = 3
        self.timeout_length = 300
        self.checkdb.start()
    
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
        date = str(datetime.today() + relativedelta(days=7)).split()
        warn_entry = (str(member.id), reason, date[0])
        c.execute("INSERT INTO warnings VALUES(?,?,?)", warn_entry)
        conn.commit()
        c.execute("SELECT warnings FROM points WHERE member=?", t)
        value = c.fetchone()
        await ctx.send(f"{member.name} has been warned!")
        if value[0] == self.warn_max:
            c.execute("UPDATE points SET warnings = 0, timeouts = timeouts + 1 WHERE member=?", t)
            c.execute("DELETE FROM warnings WHERE member = ?", t)
            conn.commit()
            await member.timeout(timedelta(seconds=self.timeout_length))
            await ctx.send(f"{member.name} got {self.warn_max} warnings and is in time out")
        conn.close()

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def warnings(self, ctx, member: discord.Member = None):
        t = (str(member.id),)
        conn = sqlite3.connect("press.db")
        c = conn.cursor()
        result = c.execute("SELECT reason FROM warnings WHERE member = ?", t)
        reasons = "\n".join(i[0] for i in result)
        c.execute("SELECT timeouts FROM points WHERE member = ?", t)
        timeouts = c.fetchone()
        text = f"Total timeouts: {timeouts[0]}\n\nCurrent warning reasons:\n{reasons}"
        embed = discord.Embed(title=member.name, description=text)
        await ctx.send(embed = embed)

    @tasks.loop(hours=1.0)
    async def checkdb(self):
        date = str(datetime.today()).split()
        date = (date[0],)
        conn = sqlite3.connect('press.db')
        c = conn.cursor()
        c2 = conn.cursor()
        result = c.execute("SELECT * FROM warnings")
        for row in result:
            if row[2] == date[0]:
                member = (row[0],)
                c2.execute("UPDATE points SET warnings = warnings - 1 WHERE member=?", member)
                conn.commit()
                c2.execute("SELECT warnings FROM points WHERE member=?", member)
                value = c2.fetchone()
                if value[0] < 0:
                    c2.execute("UPDATE points SET warnings = 0 WHERE member=?", member)
                    conn.commit()
        c.execute("DELETE FROM warnings WHERE date = ?", date)
        conn.commit()
        conn.close()
    
    @checkdb.before_loop
    async def before_checkdb(self):
        print("starting bot")
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(warning(bot))
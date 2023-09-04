from discord.ext import commands, tasks
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
import discord
import sqlite3
import utils.config as config

class warning(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warn_max = config.warn_max
        self.timeout_length = config.timeout_length
        self.checkdb.start()
        self.checktimeouts.start()

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, member: discord.Member = None):
        t = (str(member.id),)
        conn = sqlite3.connect("press.db")
        c = conn.cursor()
        in_db = c.execute("SELECT EXISTS(SELECT 1 FROM points WHERE member=?)", t).fetchone()[0]
        if in_db:
            c.execute("UPDATE points SET warnings = warnings + 1 WHERE member=?", t)
            conn.commit()
        else:
            c.execute("INSERT INTO points VALUES(?,?,?,?,?)",(str(member.id),1, 1, 0, ""))
            conn.commit()

        contents = ctx.message.content.split()
        reason = " ".join(str(i) for i in contents[2:])
        date = str(datetime.today() + relativedelta(days=config.warning_expire)).split()
        warn_entry = (str(member.id), reason, date[0])
        c.execute("INSERT INTO warnings VALUES(?,?,?)", warn_entry)
        conn.commit()
        c.execute("SELECT warnings FROM points WHERE member=?", t)
        value = c.fetchone()
        await ctx.send(f"{member.name} has been warned!")
        if value[0] == self.warn_max:
            result = c.execute("SELECT* FROM timeouts WHERE member=?", t)
            last_30_days = 0
            for row in result:
                last_30_days += 1
            c.execute("DELETE FROM warnings WHERE member = ?", t)
            c.execute("UPDATE points SET warnings = 0 WHERE member=?", t)
            conn.commit()
            await member.timeout(
                timedelta(
                    seconds=self.timeout_length * last_30_days + self.timeout_length
                )
            )
            await ctx.send(
                f"{member.name} got {self.warn_max} warnings and is in time out"
            )
        conn.close()

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def warnings(self, ctx, member: discord.Member = None):
        try:
            t = (str(member.id),)
            conn = sqlite3.connect("press.db")
            c = conn.cursor()
            result = c.execute("SELECT reason FROM warnings WHERE member = ?", t)
            reasons = "\n".join(i[0] for i in result)
            c.execute("SELECT timeouts FROM points WHERE member = ?", t)
            timeouts = c.fetchone()
            timeouts = timeouts[0]
            c.execute("SELECT lasttimeout FROM points WHERE member=?", t)
            lasttimeout = c.fetchone()
            lasttimeout = lasttimeout[0]
            results = c.execute("SELECT* FROM timeouts WHERE member=?", t)
            last_30_days = 0
            for row in results:
                last_30_days += 1
            embed = discord.Embed(
                title=member.name,
                description=f"Total timeouts:{timeouts} | Last timeout:{lasttimeout}\nLast 30 days:{last_30_days}\n\nCurrent warning reasons:\n{reasons}",
            )
            conn.close()
            await ctx.send(embed=embed)
        except TypeError:
            await ctx.send(embed=discord.Embed(title=member.name, description=f"This user has no database entry")) 


    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.is_timed_out():
            date = str(datetime.today()).split()
            futuredate = str(datetime.today() + relativedelta(days=config.timeout_expire)).split()
            t = (date[0], str(after.id))
            member = (str(after.id),)
            timeouttuple = (str(after.id), futuredate[0])
            conn = sqlite3.connect("press.db")
            c = conn.cursor()
            c.execute(
                "UPDATE points SET timeouts = timeouts + 1 WHERE member=?", member
            )
            c.execute("UPDATE points SET lasttimeout=? WHERE member=?", t)
            c.execute("INSERT INTO timeouts VALUES(?,?)", timeouttuple)
            conn.commit()
            conn.close()

    @tasks.loop(hours=24.0)
    async def checkdb(self):
        date = str(datetime.today()).split()
        date = (date[0],)
        conn = sqlite3.connect("press.db")
        c = conn.cursor()
        c2 = conn.cursor()
        result = c.execute("SELECT * FROM warnings")
        for row in result:
            if row[2] == date[0]:
                member = (row[0],)
                c2.execute(
                    "UPDATE points SET warnings = warnings - 1 WHERE member=?", member
                )
                conn.commit()
                c2.execute("SELECT warnings FROM points WHERE member=?", member)
                value = c2.fetchone()
                if value[0] < 0:
                    c2.execute("UPDATE points SET warnings = 0 WHERE member=?", member)
                    conn.commit()
        c.execute("DELETE FROM warnings WHERE date = ?", date)
        conn.commit()
        conn.close()

    @tasks.loop(hours=24.0)
    async def checktimeouts(self):
        date = str(datetime.today()).split()
        date = (date[0],)
        conn = sqlite3.connect("press.db")
        c = conn.cursor()
        c.execute("DELETE FROM timeouts WHERE date = ?", date)
        conn.commit()
        conn.close()

    @checkdb.before_loop
    async def before_checkdb(self):
        print("starting bot")
        await self.bot.wait_until_ready()

    @checktimeouts.before_loop
    async def before_timeoutcheck(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(warning(bot))

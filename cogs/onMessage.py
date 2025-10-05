from discord.ext import commands
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
import discord
import sqlite3
import utils.config as config

class onMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bad_words = []
        self.warn_max = config.warn_max
        self.timeout_length = config.timeout_length
        self.bannedlinks = "discord.gg"

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        contents = message.content.lower().split()

        if self.bannedlinks in message.content:
            if message.author.guild_permissions.ban_members == False:
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention}, you can't post discord links here"
                )

        for word in self.bad_words:
            if word in contents:
                if message.author.guild_permissions.ban_members == True:
                    return
                print(message)
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention}, message contained banned word and you have been warned."
                )
                t = (str(message.author.id),)
                conn = sqlite3.connect("press.db")
                c = conn.cursor()
                in_db = c.execute("SELECT EXISTS(SELECT 1 FROM points WHERE member=?)", t).fetchone()[0]
                if in_db:
                    c.execute("UPDATE points SET warnings = warnings + 1 WHERE member=?", t)
                    conn.commit()
                else:
                    c.execute("INSERT INTO points VALUES(?,?,?,?,?)",(str(message.author.id),1, 1, 0, ""))
                    conn.commit()
                reason = "used slur/banned word"
                date = str(datetime.today() + relativedelta(days=config.warning_expire)).split()
                warn_entry = (str(message.author.id), reason, date[0])
                c.execute("INSERT INTO warnings VALUES(?,?,?)", warn_entry)
                conn.commit()
                c.execute("SELECT warnings FROM points WHERE member=?", t)
                value = c.fetchone()
                if value[0] == self.warn_max:
                    result = c.execute(
                        "SELECT* FROM timeouts WHERE member=?", t)
                    last_30_days = 0
                    for row in result:
                        last_30_days += 1
                    c.execute("DELETE FROM warnings WHERE member = ?", t)
                    c.execute(
                        "UPDATE points SET warnings = 0 WHERE member=?", t)
                    conn.commit()
                    await message.author.timeout(
                        timedelta(
                            seconds=self.timeout_length * last_30_days
                            + self.timeout_length
                        )
                    )
                    await message.channel.send(
                        f"{message.author.name} got {self.warn_max} warnings and is in time out"
                    )
                conn.close()
                return
    
    @commands.Cog.listener()
    async def on_ready(self):
        conn = sqlite3.connect("press.db")
        c = conn.cursor()
        words = c.execute("SELECT word FROM words")
        for word in words:
            self.bad_words.append(word[0])
        print(self.bad_words)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def addword(self, ctx):
        conn = sqlite3.connect("press.db")
        for i in ctx.message.content.lower().split()[1:]:
            self.bad_words.append(i)
            word = (i,)
            c = conn.cursor()
            c.execute("INSERT INTO words VALUES(?)", word)
            conn.commit()
            await ctx.send(f"added {i}")
        conn.close()

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def deleteword(self, ctx):
        conn = sqlite3.connect("press.db")
        for i in ctx.message.content.lower().split()[1:]:
            self.bad_words.remove(i)
            word = (i,)
            c = conn.cursor()
            c.execute("DELETE FROM words WHERE word = ?", word)
            conn.commit()
            await ctx.send(f"deleted {i}")
        conn.close()

    @commands.command(aliases=["wordlist"])
    @commands.has_permissions(ban_members=True)
    async def listwords(self, ctx):
        embed = discord.Embed(title="Banned word list", description="\n".join(i for i in self.bad_words))
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(onMessage(bot))

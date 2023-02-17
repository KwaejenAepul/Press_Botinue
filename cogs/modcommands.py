from discord.ext import commands
from datetime import timedelta
import discord
import sqlite3

class mod_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warn_max = 3

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=limit)

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member = None):
        await member.ban()

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def warn(self, ctx, member: discord.Member = None):
        t = (str(member.id),)
        conn = sqlite3.connect("press.db")
        c = conn.cursor()
        c.execute("UPDATE points SET warnings = warnings + 1 WHERE member=?", t)
        conn.commit()
        c.execute("SELECT warnings FROM points WHERE member=?", t)
        value = c.fetchone()
        await ctx.send(f"{member.name} has been warned!")
        if value[0] == self.warn_max:
            await member.timeout(timedelta(seconds=60))
            await ctx.send(f"{member.name} got {self.warn_max} warnings and is in time out")
            c.execute("UPDATE points SET warnings = 0 WHERE member=?", t)
            conn.commit()
        conn.close()

async def setup(bot):
    await bot.add_cog(mod_commands(bot))
from discord.ext import commands
import discord
import sqlite3


class ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def points(self, ctx,  member: discord.Member = None):
        if member is None:
            t = (str(ctx.author.id),)
            conn = sqlite3.connect("press.db")
            c = conn.cursor()
            c.execute("SELECT pupapoints FROM points WHERE member=?", t)
            points = c.fetchone()
            await ctx.send(f"You have {points[0]} pupapoints")
        else:
            t = (str(member.id),)
            conn = sqlite3.connect("press.db")
            c = conn.cursor()
            c.execute("SELECT pupapoints FROM points WHERE member=?", t)
            points = c.fetchone()
            await ctx.send(f"{member.name} has {points[0]} pupapoints")

    @commands.command()
    async def top5(self, ctx):
        pass


async def setup(bot):
    await bot.add_cog(ranking(bot))

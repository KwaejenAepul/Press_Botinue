from discord.ext import commands
from datetime import timedelta
import discord
import sqlite3

class mod_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warn_max = 3
        self.timeout_length = 300
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=limit)
        await ctx.send(f"```{limit} messages have been purged```")

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member = None):
        await member.ban()

async def setup(bot):
    await bot.add_cog(mod_commands(bot))
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
        await ctx.channel.purge(limit=limit + 1)
        message = await ctx.send(f"```{limit} messages have been purged```")
        await message.delete(delay=3)


    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member = None):
        await member.ban()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(error)

async def setup(bot):
    await bot.add_cog(mod_commands(bot))
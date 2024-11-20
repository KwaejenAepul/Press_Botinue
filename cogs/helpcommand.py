from discord.ext import commands
import discord
from utils.config import prefix

class helpcommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def helpmod(self, ctx):
        title = "Mod commands"
        addword = f"{prefix}addword - add word or words to bad word list\n"
        deleteword = f"{prefix}deleteword - delete word or words from bad word list\n"
        listword = f"{prefix}listwords - list of bad words\n\n"
        warn = f"{prefix}warn - give a warning\n"
        warnings = f"{prefix}warnings- returns current warnings and timeout data of member\n\n"
        purge = f"{prefix}purge- removes n number of messages\n\n"
        challengeon= f"{prefix}challengeon true/false - turns on or off challenge\n"
        challengeedit = f"{prefix}editchallenge - edit the current challenge\n"
        commands = addword + deleteword + listword + warn + warnings + purge + challengeon + challengeedit
        embed = discord.Embed(title=title, description=commands)
        await ctx.send(embed=embed)

    
async def setup(bot):
    await bot.add_cog(helpcommand(bot))

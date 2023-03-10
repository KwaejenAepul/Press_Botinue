from discord.ext import commands
import discord

class helpcommand(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def helpmod(self, ctx):
        title = "Mod commands"
        addword = "!addword - add word or words to bad word list\n"
        deleteword="!deleteword - delete word or words from bad word list\n"
        listword="!listwords - list of bad words\n\n"
        warn="!warn - give a warning\n"
        warnings="!warnings- returns current warnings and timeout data of member\n\n"
        purge="!purge- removes n number of messages"
        commands = addword + deleteword + listword + warn + warnings + purge
        embed = discord.Embed(title=title, description=commands)
        await ctx.send(embed=embed)


    @commands.command(aliases = ["help"])
    async def member_help(self,ctx):
        pass

async def setup(bot):
    await bot.add_cog(helpcommand(bot))
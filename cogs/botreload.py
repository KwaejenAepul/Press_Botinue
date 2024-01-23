import utils.config
from discord.ext import commands
from os import listdir
from importlib import reload

class reloadbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def botreload(self, ctx):
        for file in listdir("./cogs"):
            try:
                if file.endswith(".py"):
                    await self.bot.reload_extension(f"cogs.{file[:-3]}")
            except:
               await self.bot.load_extension(f"cogs.{file[:-3]}")              
        reload(utils.config)
        await ctx.send("Bot has been reloaded")

async def setup(bot):
    await bot.add_cog(reloadbot(bot))
            

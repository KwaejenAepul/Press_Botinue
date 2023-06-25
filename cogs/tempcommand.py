from discord.ext import commands

class tempcommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def needstring(self, ctx):
        content = ctx.message.content.split("\"")
        for i in content:
            if i == "" or i == " ":
                content.remove(i)
        print(content)

    @commands.command()
    async def testunicode(self, ctx):
        unicodetest = ""
        i = 0
        while i < 10:
            unicodetest += f"{i}\u20e3"
            i += 1
        await ctx.send(unicodetest)
        

async def setup(bot):
    await bot.add_cog(tempcommand(bot))


from discord.ext import commands, tasks
import discord
import utils.config as config

class mod_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warn_max = config.warn_max
        self.timeout_length = config.timeout_length
        self.challenge_message = ""
        self.channelID = config.generalchatID
        self.da_rulesID = config.challengerulesID
        self.challengeMessage.start()

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit + 1)
        message = await ctx.send(f"```{limit} messages have been purged```")
        await message.delete(delay=3)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None):
        await member.ban()

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def editchallenge(self, ctx):
        self.challenge_message = " ".join(i for i in ctx.message.content.split()[1:])
        with open("challenge.txt", "w") as f:
            f.write(self.challenge_message)
        await ctx.send(f"The challenge has been set to {self.challenge_message}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def challengeon(self, ctx, boolarg: str):
        if boolarg == "true":
            self.challengeMessage.start()
            await ctx.send("challenge reminder is on")
        elif boolarg =="false":
            self.challengeMessage.stop()
            await ctx.send("challenge reminder is off")
        

    @commands.Cog.listener()
    async def on_ready(self):
        with open("challenge.txt", "r") as f:
            self.challenge_message = f.readline()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(error)
        return

    @tasks.loop(hours = config.remindertimer)
    async def challengeMessage(self):
        channel = self.bot.get_channel(self.channelID)
        da_rules = self.bot.get_channel(self.da_rulesID)
        msg = f"""
        \nCheck out this Month's Community Challenge for a chance to gain exclusive server roles.
        \nCurrently this Month's challenge is: 
        {self.challenge_message}
        \nHead on over to {da_rules.mention} for more information."""
        await channel.send(msg)

    @challengeMessage.before_loop
    async def before_checkdb(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(mod_commands(bot))

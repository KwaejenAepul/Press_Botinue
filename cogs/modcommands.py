from discord.ext import commands, tasks
import discord

#1002680285491646564
class mod_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warn_max = 3
        self.timeout_length = 300
        self.challenge_message = ""
        self.challenge_running = True
        # we hardcoding that shit LETS GOOOOOOOO
        self.channelID = 995797277027344436
        self.da_rulesID = 1007647922311155834
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
        contents = ctx.message.content.split()
        self.challenge_message = " ".join(i for i in contents[1:])
        with open("challenge.txt", "w") as f:
            f.write(self.challenge_message)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def challengeon(self, ctx):
        contents = ctx.message.content.lower().split()
        if contents[1] == "true":
            self.challenge_running = True
        elif contents[1]=="false":
            self.challenge_running = False
        print(self.challenge_running)

    @commands.Cog.listener()
    async def on_ready(self):
        with open("challenge.txt", "r") as f:
            self.challenge_message = f.readline()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(error)
        return

    @tasks.loop(hours=12.0)
    async def challengeMessage(self):
        channel = self.bot.get_channel(self.channelID)
        if self.challenge_running:
            da_rules = self.bot.get_channel(self.da_rulesID)
            msg = f"""
            \nDaily reminder to check out this Months Community Challenge for a chance to gain exclusive server roles,and a chance to win a prize.
            \nCurrently this Month's challenge is: 
            {self.challenge_message}
            \nHead on over to {da_rules.mention} for more information."""
            await channel.send(msg)
        else:
            pollID = self.bot.get_channel(1002680285491646564)
            await channel.send(f"Reminder to check out {pollID.mention} to vote on the next Community Challenge")

    @challengeMessage.before_loop
    async def before_checkdb(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(mod_commands(bot))

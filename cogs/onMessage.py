from discord.ext import commands
import discord
import sqlite3


class onMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bad_words = []
    
    #Word filter related stuff
    @commands.Cog.listener()
    async def on_ready(self):
        with open("naughtywords.txt", "r") as f:
            lines = f.readlines()
            for i in lines:   
                self.bad_words.append(i.strip())
        f.close()
        print(self.bad_words)

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def add_word(self, ctx):
        contents = ctx.message.content.split()
        word = contents[1]
        with open("naughtywords.txt", "a") as f:
            f.write(f"\n{word}")
        self.bad_words.append(word)
        print(self.bad_words)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if not message.content.startswith("!add_word"):
            contents = message.content.lower().split()
            for word in self.bad_words:
                if word in contents:
                    await message.delete()

        #Message counter
        conn = sqlite3.connect('press.db')
        c = conn.cursor()
        t = (str(message.author.id),)
        c.execute("UPDATE points SET pupapoints = pupapoints + 1 WHERE member=?", t)
        conn.commit()
        conn.close()
    

async def setup(bot):
    await bot.add_cog(onMessage(bot))
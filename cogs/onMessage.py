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
        conn = sqlite3.connect("press.db")
        c = conn.cursor()
        words = c.execute("SELECT word FROM words")
        for word in words:
            self.bad_words.append(word[0])
        print(self.bad_words)

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def addword(self, ctx):
        contents = ctx.message.content.lower().split()
        for i in contents[1:]:
            self.bad_words.append(i)
            word = (i,)
            conn = sqlite3.connect("press.db")
            c = conn.cursor()
            c.execute("INSERT INTO words VALUES(?)", word)
            conn.commit()
            conn.close()
            await ctx.send(f"added {i}")
            
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def deleteword(self, ctx):
        contents = ctx.message.content.lower().split()
        for i in contents[1:]:
            self.bad_words.remove(i)
            word = (i,)
            conn = sqlite3.connect("press.db")
            c = conn.cursor()
            c.execute("DELETE FROM words WHERE word = ?", word)
            conn.commit()
            conn.close()
            await ctx.send(f"deleted {i}")

    @commands.command(aliases = ["wordlist"])
    async def listwords(self,ctx):
        words = "\n".join(i for i in self.bad_words)
        embed = discord.Embed(title= "Banned word list", description= words)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        contents = message.content.lower().split()
        for word in self.bad_words:
            if word in contents:
                await message.delete()
                await message.channel.send(f"{message.author.mention}, message contained banned word use \"!wordlist\" for the list of bannd words")

        #Message counter
        conn = sqlite3.connect('press.db')
        c = conn.cursor()
        t = (str(message.author.id),)
        c.execute("UPDATE points SET pupapoints = pupapoints + 1 WHERE member=?", t)
        conn.commit()
        conn.close()
    

async def setup(bot):
    await bot.add_cog(onMessage(bot))
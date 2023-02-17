from discord.ext import commands
import discord
import sqlite3


class onMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        #Message counter
        conn = sqlite3.connect('press.db')
        c = conn.cursor()
        t = (str(message.author.id),)
        c.execute("UPDATE points SET pupapoints = pupapoints + 1 WHERE member=?", t)
        conn.commit()
        conn.close()
    

async def setup(bot):
    await bot.add_cog(onMessage(bot))
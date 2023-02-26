from discord.ext import commands
import discord
import sqlite3

class onjoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(member.id)
        conn = sqlite3.connect('press.db')
        c = conn.cursor()
        newmember=(str(member.id), 0, 0, 0)
        try:
            c.execute("INSERT INTO points VALUES(?,?,?,?)", newmember)
            conn.commit()
            print(f"{newmember[0]} was added")
        except:
            print(f"{newmember} could not be added")
        conn.close()

async def setup(bot):
    await bot.add_cog(onjoin(bot))
from discord.ext import commands
import discord
import sqlite3

class database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def init_db(self, ctx):
        conn = sqlite3.connect('press.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS points (member UNIQUE , pupapoints INT, warnings INT)''')
        for i in ctx.guild.members:
            if i.id == bot.user.id:
                pass
            else:
                try:
                    c.execute("INSERT INTO points VALUES(?,?,?)", (str(i.id), 0, 0))
                    conn.commit()
                except:
                    print(f"couldn't add {i.id}")
        conn.close()

async def setup(bot):
    await bot.add_cog(database(bot))
from discord.ext import commands
import discord
import sqlite3

class leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def init_leaderboards(self, ctx):
        conn = sqlite3.connect("leaderboards.db")
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS leaderboard (member UNIQUE, points INT)"""
        )
        conn.commit()
        conn.close()
        await ctx.send("leaderboard initialized")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def new_entry(self, ctx):
        conn = sqlite3.connect("leaderboards.db")
        c = conn.cursor()
        i=1
        contents = ctx.message.content.split()
        for member in contents[1:] :
            points = 0
            member = int(member)
            if i == 1:
                points = 3
            elif i == 2:
                points = 2
            elif i == 3:
                points = 1
            else:
                break
            in_db = c.execute("SELECT EXISTS(SELECT 1 FROM leaderboard WHERE member = ?)", (member,)).fetchone()[0]
            if in_db:
                c.execute("UPDATE leaderboard SET points + ? WHERE member=?", (points, member))
            else:
                c.execute("INSERT INTO leaderboard VALUES(?,?)", (member, points))
            i+=1
            conn.commit()
        conn.close()

    @commands.command()
    async def leaderboards(self, ctx):
        conn = sqlite3.connect("leaderboards.db")
        c = conn.cursor()
        results = c.execute("SELECT member, points FROM leaderboard ORDER BY points DESC").fetchall()
        print(f"{results}")
        conn.close()

async def setup(bot):
    await bot.add_cog(leaderboard(bot))


# файл для тестовых команд
import discord
from discord.ext import commands
import sqlite3

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

allowed_users = [695684705328169060, 617415875947003915]

class Test(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def репутация(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(embed = discord.Embed(
                description=f'Репутация пользователя __**{ctx.author}**__ равна __**{cursor.execute("SELECT rep FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**__',
                color = discord.Colour.random()
            ))
        else:
            await ctx.send(embed = discord.Embed(
                description=f'Репутация пользователя __**{member}**__ равна __**{cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0]}**__',
                color = discord.Colour.random()
            ))
    

async def setup(client):
    await client.add_cog(Test(client))
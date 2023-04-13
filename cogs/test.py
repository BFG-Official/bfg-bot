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
    async def тест(self, ctx):
        await ctx.send(embed = discord.Embed(
            description = f'[Сообщение](https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id})'
        ))

    @commands.command()
    async def тест2(self, ctx):
        await ctx.send(embed = discord.Embed(
            description = 'Секретный тест'
        ))

async def setup(client):
    await client.add_cog(Test(client))
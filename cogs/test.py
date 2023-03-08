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

async def setup(client):
    await client.add_cog(Test(client))
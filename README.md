гитхаб очень просил чтобы я добавил этот файл

При создании новой группы команд:
Создаём файл название.py В ПАПКУ "cogs" и используем шаблон:
============================================================================
import discord
from discord.ext import commands

class Название(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    (Здесь команды)

def setup(client):
    client.add_cog(Название как в class(client))
============================================================================
"@bot.command" мнеяется на "@commands.command()"
"@bot.event" мнеяется на "@commands.Cog.listener()"

Некоторые функции например ".get_channel(id)" могут не работать
Для исправления можно попробовать дописать ".get_channel(self.client, id)"

Приписка "bot." (bot.get_channel(id)) меняется на "command.Bot"

Если создавать новую команду то надо обязательно добавлять 'self'
Как ненадо: "async def хелп(ctx)"
Как надо: "async def хелп(self, ctx)"
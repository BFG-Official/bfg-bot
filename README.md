# При создании новой группы команд:
## Создаём файл название.py В ПАПКУ "cogs" и используем шаблон:


```
import discord
from discord.ext import commands

class Название(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    (Здесь код)

async def setup(client):
    await client.add_cog(Название(client))
```

"@bot.command" меняется на "@commands.command()"
"@bot.event" меняется на "@commands.Cog.listener()"

Некоторые функции например ".get_channel(id)" могут не работать,
для исправления можно попробовать дописать ".get_channel(self.client, id)"

Приписка "bot." (bot.get_channel(id)) меняется на "command.Bot"

Если создавать новую команду то надо обязательно добавлять 'self':

Как неправильно: "async def название_команды(ctx)",
Как правильно: "async def название_команды(self, ctx)"

# При создании эмбеда добавлять в конец следующее:
`.set_footer(
            text = f'{ctx.author} вызвал команду',
            icon_url = ctx.author.avatar.url
        )`

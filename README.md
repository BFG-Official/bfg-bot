# При создании новой группы команд:

Создайте файл с названием.py в папке "cogs" и используйте шаблон:

```py
import discord
from discord.ext import commands

class Название(commands.Cog):

    def __init__(self, client):
        self.client = client
    
# Здесь код

async def setup(client):
    await client.add_cog(Название(client))
```

- При создании команды используйте `ctx.message.reply` вместо `ctx.send` (Используйте только в случаях, когда нужно ответить пользователю, например, сообщение о том, что пользователь не указал какой-либо аргумент, или об успешном выполнении команды).
- Замените `@bot.command` на `@commands.command()` и `@bot.event` на `@commands.Cog.listener()`.
- Обязательно добавьте `@commands.guild_only()` после `@commands.command()` при создании команды.
- Некоторые функции, например `.get_channel(id)`, могут не работать. Чтобы исправить это, вы можете дописать `.get_channel(self.client, id)`.
- Замените `bot.` (bot.get_channel(id)) на `command.Bot`.
- Если вы создаете новую команду, то обязательно добавьте `self`:

**Неправильно:** "async def название_команды(ctx)"

**Правильно:** "async def название_команды(self, ctx)"

- При создании эмбеда добавьте следующее в конце:
```py
.set_footer(text=f'{ctx.author} вызвал команду', icon_url=ctx.author.avatar.url)
```

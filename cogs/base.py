import discord
from discord.ext import commands
import pytz, datetime, asyncio

class Base(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def хелп(self, ctx):
        embed = discord.Embed(
            title = '**Список команд**',
            description = '`>привет` - Приветствие бота\n`>повтори (сообщение)` - Бот повторит ваше сообщение\n`>очистить (кол-во)` - Бот очистит некоторое количество сообщений\n`>напомни (ДД.ММ.ГГ_ЧЧ:ММ) (текст)` - Бот напомнит в определённую дату\n`>тестэмбед` - тестовый эмбед',
            color = discord.Colour.random()
        )

        await ctx.send(embed = embed)
    
    @commands.command()
    async def привет(self, ctx):
        await ctx.send(f'Приветик, {ctx.message.author.mention}!')
    
    @commands.command()
    async def повтори(self, ctx, *, arg):
        await ctx.send(arg)
    
    @commands.command()
    async def напомни(self, ctx, ttime, *, text = 'None'):
        try:
            n = ttime + '+0300'
            a = datetime.datetime.strptime(n, '%d.%m.%Y_%H:%M%z')
            t = datetime.datetime.now(pytz.timezone("Europe/Moscow"))
            sa = a.timestamp()
            st = t.timestamp()
            time = int(sa) - int(st)
            if time > 0:
                message = await ctx.reply('Напоминание сработает <t:' + str(int(sa)) + ':R>')
                edit = 'Напоминание сработало <t:' + str(int(sa)) + ':R>'
                while time != 0:
                    time -= 1
                    print(time,text)
                    await asyncio.sleep(1)
                if text == 'None':
                    await message.edit(content = edit)
                    await ctx.reply('Напоминание без текста')
                else:
                    await message.edit(content = edit)
                    await ctx.reply(ctx.message.author.mention + ', ' + text)
            else:
                await ctx.send('Пишите **будущую московскую** дату')
        except:
            await ctx.send('Пиши `>напомни (ДД.ММ.ГГ_ЧЧ:ММ) (текст)`. Писать **будущую московскую** дату')


async def setup(client):
    await client.add_cog(Base(client))
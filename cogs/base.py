import discord
from discord.ext import commands
import pytz, datetime, asyncio, sqlite3

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

class Base(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def хелп(self, ctx):
        embed = discord.Embed(
            title = '**Список команд**',
            description = '`>привет` - Приветствие бота\n`>очистить (кол-во)` - Бот очистит некоторое количество сообщений\n`>напомни (ДД.ММ.ГГ_ЧЧ:ММ) (текст)` - Бот напомнит в определённую дату\n`>репутация` - Бот покажет вашу репутпцию\n`>топ (название)` - Бот покажет таблицу лидеров',
            color = discord.Colour.random()
        )

        await ctx.send(embed = embed)

    @commands.command()
    async def топ(self, ctx, name :str = None):
        if name is None: await ctx.send('Укажите название таблицы топов (репутации)')
        if not (name in ['репутации']): await ctx.send('Такого названия таблицы лидеров не существует')
        if name == 'репутации':
            k = 0
            s = ''
            for top_rep in cursor.execute("SELECT id, rep FROM users ORDER BY rep DESC LIMIT 10"):
                k += 1
                s = s + f'{k}) __**{commands.Bot.get_user(self.client, top_rep[0])}**__ | __**{top_rep[1]}**__ репутации(-ия)\n'
            await ctx.send(embed = discord.Embed(
                title = '**Топ репутаций**',
                description = s,
                color = discord.Colour.random()
            ))
    
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
    
    @commands.command()
    async def привет(self, ctx):
        await ctx.send(f'Приветик, {ctx.message.author.mention}!')

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
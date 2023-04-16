import discord
from typing import Union
from discord.ext import commands
import pytz, datetime, asyncio, sqlite3, requests

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

class commands_base(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.guild_only()
    async def хелп(self, ctx):
        embed = discord.Embed(
            title='**Список команд**',
            description='**Основные команды**\n\n'
                        '`>напомни (ДД.ММ.ГГ_ЧЧ:ММ) (текст)` - '
                        'Бот напомнит в определённую дату,\n'
                        '`>репутация` - Бот покажет вашу репутпцию,\n'
                        '`>топ (название)` - Бот покажет таблицу лидеров,\n'
                        '`>серверинфо` - Выводит информацию о сервере.\n\n'
                        '**Разное**\n\n'
                        '`>привет` - Приветствие бота,\n'
                        '`>инфо (ID или оставить пустым)` - Информация о пользователе.\n'
                        '`>кот` - Рандомная картинка кота.\n'
                        '`>пёс` - Рандомная картинка пса.',
            color=discord.Colour.random()
        )
        embed.set_footer(text=f'{ctx.author} вызвал команду', icon_url=ctx.author.avatar.url)
        await ctx.message.reply(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def топ(self, ctx, name :str = None):
        if name is None: await ctx.message.reply('Укажите название таблицы топов (репутации)')
        if not (name in ['репутации']): await ctx.message.reply('Такого названия таблицы лидеров не существует')
        if name == 'репутации':
            k = 0
            s = ''
            for top_rep in cursor.execute("SELECT id, rep FROM users ORDER BY rep DESC LIMIT 10"):
                k += 1
                s = s + f'{k}) __**{commands.Bot.get_user(self.client, top_rep[0])}**__ | __**{top_rep[1]}**__ репутации(-ия)\n'
            s = s + '...'
            k = int(ctx.guild.member_count)
            s2 = ''
            for top_rep in cursor.execute("SELECT id, rep FROM users ORDER BY rep ASC LIMIT 10"):
                s2 = f'\n{k}) __**{commands.Bot.get_user(self.client, top_rep[0])}**__ | __**{top_rep[1]}**__ репутации(-ия)' + s2
                k -= 1
            
            await ctx.message.reply(embed = discord.Embed(
                title = '**Топ репутаций**',
                description = s + s2,
                color = discord.Colour.random()
            ).set_footer(
            text = f'{ctx.author} вызвал команду',
            icon_url = ctx.author.avatar.url
            ))
    
    @commands.command()
    @commands.guild_only()
    async def репутация(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.message.reply(embed = discord.Embed(
                description=f'Репутация пользователя __**{ctx.author}**__ равна __**{cursor.execute("SELECT rep FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**__',
                color = discord.Colour.random()
            ).set_footer(
            text = f'{ctx.author} вызвал команду',
            icon_url = ctx.author.avatar.url
            ))
        else:
            await ctx.send(embed = discord.Embed(
                description=f'Репутация пользователя __**{member}**__ равна __**{cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0]}**__',
                color = discord.Colour.random()
            ).set_footer(
            text = f'{ctx.author} вызвал команду',
            icon_url = ctx.author.avatar.url
            ))
    
    @commands.command()
    @commands.guild_only()
    async def привет(self, ctx):
        await ctx.message.reply(f'Приветик, {ctx.message.author.mention}!')

    @commands.command()
    @commands.guild_only()
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
                await ctx.message.reply('Пишите **будущую московскую** дату')
        except:
            await ctx.message.reply('Пиши `>напомни (ДД.ММ.ГГ_ЧЧ:ММ) (текст)`. Писать **будущую московскую** дату')

    @commands.command()
    @commands.guild_only()
    async def инфо(self, ctx, member: Union[discord.Member, int, str] = None):
        
        if member is None:
            member = ctx.author
        elif isinstance(member, str):
            return await ctx.message.reply('Аргумент должен быть числом!')
        elif isinstance(member, int):
            try:
                member = await ctx.guild.fetch_member(member)
            except discord.NotFound:
                return await ctx.message.reply('Пользователь с таким ID не найден!')
        elif not isinstance(member, discord.Member):
            return await ctx.message.reply('Неверный тип аргумента!')
        
        embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
        embed.set_author(name=f"Информация о пользователе - {member}")
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="ID:", value=member.id, inline=True)
        embed.add_field(name="Имя:", value=member.display_name, inline=True)
        embed.add_field(name="Аккаунт создан в:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=True)
        
        if isinstance(member, int):
            age = None
        else:
            age = (ctx.message.created_at - member.created_at).days // 365
        embed.add_field(name="Возраст аккаунта:", value=f"{age} {'год' if age == 1 else 'года' if 1 < age < 5 else 'лет'}", inline=True)
        embed.set_footer(text=f'{ctx.author} вызвал команду', icon_url=ctx.author.avatar.url)
        await ctx.message.reply(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def серверинфо(self, ctx):
        all_members = len(ctx.guild.members)
        humans = len(list(filter(lambda m: not m.bot, ctx.guild.members)))
        bots = len(list(filter(lambda m: m.bot, ctx.guild.members)))

        online = len(list(filter(lambda m: m.status == discord.Status.online, ctx.guild.members)))
        idle = len(list(filter(lambda m: m.status == discord.Status.idle, ctx.guild.members)))
        dnd = len(list(filter(lambda m: m.status == discord.Status.dnd, ctx.guild.members)))
        offline = len(list(filter(lambda m: m.status == discord.Status.offline, ctx.guild.members)))

        all_channels = len(ctx.guild.channels)
        text_channels = len(ctx.guild.text_channels)
        announcement_channels = len(list(filter(lambda c: isinstance(c, discord.TextChannel) and c.is_news(), ctx.guild.channels)))
        voice_channels = len(ctx.guild.voice_channels)

        created_at = ctx.guild.created_at.strftime('%d.%m.%Y %H:%M:%S')

        owner = ctx.guild.owner

        embed = discord.Embed(title=f'Информация о сервере {ctx.guild.name}', color=discord.Color.blue())
        embed.add_field(name='Участники', value=f'Всего: {all_members}\nЛюдей: {humans}\nБотов: {bots}', inline=True)
        embed.add_field(name='По статусам', value=f'В сети: {online}\nНе активен: {idle}\nНе беспокоить: {dnd}\nНе в сети: {offline}', inline=True)
        embed.add_field(name='Каналы', value=f'Всего: {all_channels}\nТекстовых: {text_channels}\nОбъявления: {announcement_channels}\nГолосовых: {voice_channels}', inline=True)
        embed.add_field(name='Владелец', value=owner.mention, inline=True)
        embed.add_field(name='Дата создания', value=created_at, inline=True)
        embed.set_footer(text=f'{ctx.author} вызвал команду', icon_url=ctx.author.avatar.url)
        await ctx.message.reply(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def кот(self, ctx):
        response = requests.get('https://api.thecatapi.com/v1/images/search')
        data = response.json()
        image_url = data[0]['url']
        embed = discord.Embed(title='Ваш котик на подходе!', color=0xff9900)
        embed.set_image(url=image_url)
        embed.set_footer(text=f'{ctx.author} вызвал команду', icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def пёс(self, ctx):
        response = requests.get('https://api.thedogapi.com/v1/images/search')
        data = response.json()
        image_url = data[0]['url']
        embed = discord.Embed(title='Ваш пёсик на подходе!', color=0xff9900)
        embed.set_image(url=image_url)
        embed.set_footer(text=f'{ctx.author} вызвал команду', icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed)

async def setup(client):
    await client.add_cog(commands_base(client))
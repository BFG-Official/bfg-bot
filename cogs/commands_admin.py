import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

allowed_users = [695684705328169060, 617415875947003915, 784783094434758676]
allowed_roles = [964807055980523520]
moderator_roles = [1030023894968565821, 964807055980523520, 854993494107750402, 960495606596517931, 873268262555750471, 975329806520553503, 1050457595963523203]
mapchecker_role = [1068946458201575605]

class commands_admin(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.guild_only()
    async def очистить(self ,ctx, count):
        if ctx.channel.id != 1075332621095153764:
            return await ctx.message.reply('Данная команда отключена в этом канале.')

        if not ctx.message.author.guild_permissions.administrator and ctx.message.author.id not in allowed_users:
            return await ctx.message.reply('У вас нет доступа к этой команде!')
        try: count = int(count)
        except: return await ctx.message.reply('Надо писать число')
        if not (count > 0 and count <= 100): return await ctx.message.reply('Количество сообщений разрешено не менее 1 и не более 100.')
        try:
            await ctx.channel.purge(limit=count+1)
        except:
            await ctx.message.reply('Кажется я не могу удалять сообщения')

    @commands.command()
    @commands.guild_only()
    async def повтори(self, ctx, *, text):
        if not ctx.message.author.guild_permissions.administrator and ctx.message.author.id not in self.allowed_users:
            return await ctx.message.reply('У вас нет доступа к этой команде!')

        await ctx.send(text)
        await ctx.message.delete()
    
    @commands.command()
    @commands.guild_only()
    async def измрепут(self, ctx, member: discord.Member = None, amount: int = None, *, reason: str = 'Без причины'):
        if not (ctx.author.id in allowed_users): return await ctx.message.reply('У вас нет доступа!')
        if member is None: return await ctx.message.reply('Укажите пользователя `?измрепут (@участник) (репутация (может быть отрицательной)) (причина)`')
        if member.bot: return await ctx.message.reply('У ботов нет рейтинга')
        if amount is None: return await ctx.message.reply('Укажите на сколько изменить репутацию')
        cursor.execute("UPDATE users SET rep = rep + {} WHERE id = {}".format(amount, member.id))
        connection.commit()
        rep = int(cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0])
        if amount < 0:  
            await commands.Bot.get_channel(self.client, 1082613972617936926).send(embed = discord.Embed(
                description=f'Репутация __**{member}**__ понижена до __**{rep}**__ | `{amount}`\n\nРепутация была изменена администрацией сервера',
                color = discord.Colour.red()
            ))
            await ctx.message.reply(embed = discord.Embed(
                description=f'Репутация __**{member}**__ понижена до __**{rep}**__ | `{amount}`\n\nРепутация была изменена администрацией сервера',
                color = discord.Colour.red()
            ).set_footer(
            text = f'{ctx.author} вызвал команду',
            icon_url = ctx.author.avatar.url
            ))
            return
        if amount > 0:
            await commands.Bot.get_channel(self.client, 1082613972617936926).send(embed = discord.Embed(
                description=f'Репутация __**{member}**__ повышена до __**{rep}**__ | `+{amount}`\n\nРепутация была изменена администрацией сервера',
                color = discord.Colour.green()
            ))
            await ctx.message.reply(embed = discord.Embed(
                description=f'Репутация __**{member}**__ повышена до __**{rep}**__ | `+{amount}`\n\nРепутация была изменена администрацией сервера',
                color = discord.Colour.green()
            ).set_footer(
            text = f'{ctx.author} вызвал команду',
            icon_url = ctx.author.avatar.url
            ))
            return
    
    @commands.command()
    @commands.guild_only()
    async def cleardb(self, ctx, namedb: str = None, *, reason: str = 'Без причины'):
        if not (ctx.author.id in allowed_users): return await ctx.message.reply('У вас нет доступа!')
        if namedb is None: return await ctx.message.reply('Вы не указали тип переменной `?cleardb (тип)`')
        if not (namedb in ['rep', 'lvl', 'bankcash', 'cash']): return await ctx.message.reply('Существуют только `rep, lvl, bankcash, cash`')
        cursor.execute("UPDATE users SET {} = 0".format(namedb))
        connection.commit()
        await ctx.message.reply(embed = discord.Embed(
            description=f'Переменная __**{namedb}**__ обнулена у всех участников по причине __**{reason}**__',
            color = discord.Colour.random()
        ).set_footer(
            text = f'{ctx.author} вызвал команду',
            icon_url = ctx.author.avatar.url
        ))
    
    @commands.command()
    @commands.guild_only()
    async def changedb(self, ctx, namedb: str = None, member: discord.Member = None, changed = None, *, reason: str = 'Без причины'):
        if not (ctx.author.id in allowed_users): return await ctx.message.reply('У вас нет доступа!')
        if namedb is None: return await ctx.message.reply('Вы не указали тип переменной `?changedb (тип) (@участник) (на что изменить) (причина)`')
        if not (namedb in ['rep', 'lvl', 'bankcash', 'cash']): return await ctx.send('Существуют только типы `rep, lvl, bankcash, cash`')
        if namedb in ['rep', 'lvl', 'bankcash', 'cash']:
            try: changed = int(changed)
            except: return await ctx.message.reply('Для этих переменных значение должно быть число')
        cursor.execute("UPDATE users SET {} = '{}' WHERE id = {}".format(namedb, changed, member.id))
        connection.commit()
        await ctx.message.reply(embed = discord.Embed(
            description=f'Переменная __**{namedb}**__ у участника __**{member}**__ изменена на __**{changed}**__ по причине __**{reason}**__',
            color = discord.Colour.random()
        ).set_footer(
            text = f'{ctx.author} вызвал команду',
            icon_url = ctx.author.avatar.url
        ))

async def setup(client):
    await client.add_cog(commands_admin(client))
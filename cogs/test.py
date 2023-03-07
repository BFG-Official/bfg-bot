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
    
    '''@commands.command()
    async def измрепут(self, ctx, member: discord.Member = None, amount: int = None, *, reason: str = 'Без причины'):
        if not (ctx.author.id in allowed_users): return ctx.send('У вас нет доступа!')
        if member is None: return ctx.send('Укажите пользователя `>измрепут (@участник) (репутация (может быть отрицательной)) (причина)`')
        if member.bot: return ctx.send('У ботов нет рейтинга')
        if amount is None: return ctx.send('Укажите на сколько изменить репутацию')
        cursor.execute("UPDATE users SET rep = rep + {} WHERE id = {}".format(amount, member.id))
        connection.commit()
        rep = int(cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0])
        if amount < 0:  
            await commands.Bot.get_channel(self.client, 1082613972617936926).send(embed = discord.Embed(
                description=f'Репутация __**{member}**__ понижена до __**{rep}**__ | `{amount}`',
                color = discord.Colour.red()
            ))
            await ctx.reply(embed = discord.Embed(
                description=f'Репутация __**{member}**__ понижена до __**{rep}**__ | `{amount}`',
                color = discord.Colour.red()
            ))
            return
        if amount > 0:
            await commands.Bot.get_channel(self.client, 1082613972617936926).send(embed = discord.Embed(
                description=f'Репутация __**{member}**__ повышена до __**{rep}**__ | `+{amount}`',
                color = discord.Colour.green()
            ))
            await ctx.reply(embed = discord.Embed(
                description=f'Репутация __**{member}**__ повышена до __**{rep}**__ | `+{amount}`',
                color = discord.Colour.green()
            ))
            return'''


    
    

async def setup(client):
    await client.add_cog(Test(client))
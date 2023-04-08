import discord
from discord.ext import commands
import datetime, sqlite3

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in [1048466435556515890, 1048513739558752276]: return
        if message.author.bot: return
        mess = message.content.lower()
        mess = ' ' + mess.replace('||','').replace('*','').replace('_','').replace('-','').replace('.','').replace('!','').replace('?','').replace('"','').replace("'","").replace('`','').replace('⠀','') + ' '
        for p in ['п','П','π','p','P','n']:
            for o in ['о','О','o','O','0','ο']:
                for n in ['н','Н','n','N','H','H']:
                    if (' ' + p + o + n + ' ' in mess):
                        await message.reply('пидораст ты', mention_author=True)
    
    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        if payload.channel_id in [1048466435556515890, 1048513739558752276]: return
        message = await commands.Bot.get_channel(self.client, payload.channel_id).fetch_message(payload.message_id)
        mess = payload.data['content']
        mess = ' ' + mess.replace('||','').replace('*','').replace('_','').replace('-','').replace('.','').replace('!','').replace('?','').replace('"','').replace("'","").replace('`','').replace('⠀','') + ' '
        for p in ['п','П','π','p','P','n']:
            for o in ['о','О','o','O','0','ο']:
                for n in ['н','Н','n','N','H']:
                    if (' ' + p + o + n + ' ' in mess):
                        await message.reply('пидораст ты', mention_author=True)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Вы не указали все аргументы. Для помощи используйте команду >help.')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send('Пользователь не найден.')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Неправильный аргумент. Для помощи используйте команду >help.')
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send('Эта команда не может быть выполнена в личных сообщениях.')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'Эта команда недоступна. Пожалуйста, подождите {error.retry_after:.2f} секунд и попробуйте снова.')
        else:
            embed = discord.Embed(title='Ошибка выполнения команды', color=discord.Color.red())
            embed.add_field(name='Сообщение об ошибке:', value=f'```{error}```')
            embed.add_field(name='Команда:', value=f'```{ctx.message.content}```')
            embed.add_field(name='Автор:', value=f'{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})')
            embed.add_field(name='Канал:', value=f'{ctx.channel.name} ({ctx.channel.id})')
            embed.timestamp = datetime.datetime.utcnow()
            error_channel = self.client.get_channel(1077307732757057656)
            await error_channel.send(embed=embed)

async def setup(client):
    await client.add_cog(Events(client))
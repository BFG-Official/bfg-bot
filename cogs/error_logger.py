import discord
from discord.ext import commands
import datetime, sqlite3

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

class error_logger(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.reply('Вы не указали все аргументы. Для помощи используйте команду **>хелп**.')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.message.reply('Пользователь не найден.')
        elif isinstance(error, commands.BadArgument):
            await ctx.message.reply('Неправильный аргумент. Для помощи используйте команду **>хелп**.')
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.message.reply('Эта команда не может быть выполнена в личных сообщениях.')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.message.reply(f'Эта команда недоступна. Пожалуйста, подождите {error.retry_after:.2f} секунд и попробуйте снова.')
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
    await client.add_cog(error_logger(client))
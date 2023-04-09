import discord
from discord.ext import commands
import datetime

class ErrorLogger(commands.Cog):

    def __init__(self, client):
        self.client = client

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
            if error_channel:
                await error_channel.send(embed=embed)

def setup(client):
    client.add_cog(ErrorLogger(client))
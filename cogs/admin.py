import discord
from discord.ext import commands

allowed_users = [695684705328169060, 617415875947003915]
allowed_roles = [964807055980523520]
moderator_roles = [1030023894968565821, 964807055980523520, 854993494107750402, 960495606596517931, 873268262555750471, 975329806520553503, 1050457595963523203]
mapchecker_role = [1068946458201575605]

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def очистить(self ,ctx, count):
        if not ctx.message.author.guild_permissions.administrator: return await ctx.send('У вас нет доступа к этой команде!')
        try: count = int(count)
        except: return await ctx.send('Надо писать число')
        if not (count > 0 and count <= 100): return await ctx.send('Количество сообщений разрешено не менее 1 и не более 100.')
        try:
            await ctx.channel.purge(limit=count+1)
        except:
            await ctx.send('Кажется я не могу удалять сообщения')
    
def setup(client):
    client.add_cog(Admin(client))
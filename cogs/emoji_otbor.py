import discord
import textwrap
from discord.ext import commands

allowed_users = [695684705328169060, 617415875947003915, 784783094434758676]

class emoji_otbor(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def добавить_реакции(self, ctx, channel_id: int):
        if not ctx.message.author.guild_permissions.administrator and ctx.message.author.id not in self.allowed_users:
            return await ctx.send('У вас нет доступа к этой команде!')

        channel = self.client.get_channel(channel_id)
        if not channel:
            return await ctx.send("Неверный ID канала.")

        async for message in channel.history(limit=None):
            await message.add_reaction('✅')
            await message.add_reaction('❌')

        await ctx.send("Реакции добавлены на все сообщения в указанном канале.")

async def setup(client):
    await client.add_cog(emoji_otbor(client))
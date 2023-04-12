import discord
import textwrap
from discord.ext import commands

allowed_users = [695684705328169060, 617415875947003915, 784783094434758676]

class emoji_otbor(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def count_reactions(self, channel):
        # создаем словарь, где ключи - содержание сообщений, значения - словари,
        # где ключи - реакции, значения - количество реакций
        messages_reactions = {}
        async for message in channel.history(limit=None):
            if message.author.bot:
                continue
            content = message.content
            if not content:
                content = "EMPTY MESSAGE"
            if content not in messages_reactions:
                messages_reactions[content] = {}
            for reaction in message.reactions:
                if reaction.emoji in messages_reactions[content]:
                    messages_reactions[content][reaction.emoji] += reaction.count - 1
                else:
                    messages_reactions[content][reaction.emoji] = reaction.count - 1
        return messages_reactions

    @commands.command()
    async def статистика(self, ctx, channel_id: int):
        channel = self.client.get_channel(channel_id)
        if not channel:
            return await ctx.send("Канал не найден!")
        if not isinstance(channel, discord.TextChannel):
            return await ctx.send("Неверный тип канала!")
        if not ctx.message.author.guild_permissions.administrator and ctx.message.author.id not in self.allowed_users:
            return await ctx.send('У вас нет доступа к этой команде!')

        messages_reactions = await self.count_reactions(channel)
        if not messages_reactions:
            return await ctx.send("В этом канале нет сообщений!")
        
        message = []
        for content, reactions in messages_reactions.items():
            line = []
            for emoji, count in reactions.items():
                line.append(f"{count} {emoji}")
            message.append(f" ({content}) - {', '.join(line)}")
        await ctx.send("\n".join(message))

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
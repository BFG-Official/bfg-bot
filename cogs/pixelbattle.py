import discord
from discord.ext import commands

class pixelbattle(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 1093810191155343360 and payload.emoji.name == '⚒️':
            message = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)
            member = message.guild.get_member(payload.user_id)
            role = message.guild.get_role(1093252309712109568)
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 1093810191155343360 and payload.emoji.name == '⚒️':
            guild = await self.client.fetch_guild(payload.guild_id)
            member = await guild.fetch_member(payload.user_id)
            role = guild.get_role(1093252309712109568)
            await member.remove_roles(role)

async def setup(client):
    await client.add_cog(pixelbattle(client))

import discord
from discord.ext import commands, tasks
import psutil

class system_status(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.update_stats.start()
        self.message_id = 1108251841667530786

    def cog_unload(self):
        self.update_stats.cancel()

    @tasks.loop(seconds=5)
    async def update_stats(self):
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        total_memory = psutil.virtual_memory().total

        channel = self.client.get_channel(1108251768992837734)
        message = await channel.fetch_message(self.message_id)
        embed = discord.Embed(title="System Status", color=discord.Color.blue())
        embed.add_field(name="ЦП", value=f"{cpu_usage}%")
        embed.add_field(name="ОЗУ", value=f"{ram_usage}%")
        embed.add_field(name="Всего памяти", value=f"{total_memory} байт")
        await message.edit(embed=embed)

async def setup(client):
    await client.add_cog(system_status(client))
import discord
from discord.ext import commands, tasks
import psutil

class system_status(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.update_stats.start()
        self.message_id = 1108255106585071626

    def cog_unload(self):
        self.update_stats.cancel()

    @tasks.loop(seconds=5)
    async def update_stats(self):
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        processes = sorted(psutil.process_iter(['name', 'memory_info']), key=lambda p: p.info.memory_info.rss, reverse=True)
        top_processes = processes[:5]

        channel = self.client.get_channel(1108251768992837734)
        message = await channel.fetch_message(self.message_id)

        embed = discord.Embed(title="System Status", color=discord.Color.blue())
        embed.add_field(name="ЦП", value=f"{cpu_usage}%")
        embed.add_field(name="ОЗУ", value=f"{ram_usage}%")

        process_info = "\n".join([f"{p.info.name}: {p.info.memory_info.rss} bytes" for p in top_processes])
        embed.add_field(name="Самые жрущие процессы", value=process_info)

        await message.edit(embed=embed)

async def setup(client):
    await client.add_cog(system_status(client))
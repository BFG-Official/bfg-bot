import discord
from discord.ext import commands, tasks
import psutil

class SystemStatus(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.update_stats.start()
        self.message_id = 1108255106585071626

    def cog_unload(self):
        self.update_stats.cancel()

    @tasks.loop(seconds=10)
    async def update_stats(self):
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        total_memory = round(psutil.virtual_memory().total / 1024 / 1024)
        processes = sorted(psutil.process_iter(['name', 'memory_info']), key=lambda p: p.info['memory_info'].rss, reverse=True)
        top_processes = processes[:10]

        channel = self.client.get_channel(1108251768992837734)
        message = await channel.fetch_message(self.message_id)

        embed = discord.Embed(title="Статус системы", color=discord.Color.blue())
        embed.add_field(name="Использование ЦП", value=f"{cpu_usage}%")
        embed.add_field(name="Использование ОЗУ", value=f"{ram_usage}%")
        embed.add_field(name="Общий объем памяти", value=f"{total_memory} МБ")

        process_info = "\n".join([f"{p.info['name']}: {round(p.info['memory_info'].rss / 1024 / 1024)} МБ" for p in top_processes])
        embed.add_field(name="Процессы с наибольшим использованием памяти", value=process_info)

        await message.edit(embed=embed)

async def setup(client):
    await client.add_cog(SystemStatus(client))

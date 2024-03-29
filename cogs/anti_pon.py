import discord
from discord.ext import commands
import sqlite3

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

allowed_users = [695684705328169060, 617415875947003915]

class anti_pon(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in [1048466435556515890, 1048513739558752276]: return
        pon_words = []
        for p in ['п','П','π','p','P','n']:
            for o in ['о','О','o','O','0','ο']:
                for n in ['н','Н','n','N','h','H']:
                    pon_words.append(p + o + n)
        if message.author.bot: return
        mess = message.content.lower()
        mess = ' ' + mess.replace('||','').replace('*','').replace('_','').replace('-','').replace('.','').replace('!','').replace('?','').replace('"','').replace("'","").replace('`','').replace('⠀','') + ' '
        for i in pon_words:
            if (' ' + i + ' ' in mess):
                await message.reply('пидораст ты', mention_author=True)
                break #БЕБРОЧКА
    
    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        if payload.channel_id in [1048466435556515890, 1048513739558752276]: return
        pon_words = []
        for p in ['п','П','π','p','P','n']:
            for o in ['о','О','o','O','0','ο']:
                for n in ['н','Н','n','N','h','H']:
                    pon_words.append(p + o + n)
        message = await commands.Bot.get_channel(self.client, payload.channel_id).fetch_message(payload.message_id)
        mess = payload.data.get('content')
        if mess is None:
            return
        mess = ' ' + mess.replace('||','').replace('*','').replace('_','').replace('-','').replace('.','').replace('!','').replace('?','').replace('"','').replace("'","").replace('`','').replace('⠀','') + ' '
        for i in pon_words:
            if (' ' + i + ' ' in mess):
                await message.reply('пидораст ты', mention_author=True)
                break

async def setup(client):
    await client.add_cog(anti_pon(client))
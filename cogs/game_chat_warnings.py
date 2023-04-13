from discord.ext import commands

words = ['даун', 'долбaёб', 'долбаеб', 'нaхуй', 'дауних', 'ебaл', 'шлюх', 'пидор', 'пидорaс', 'негрил', 'хуесос', 'хуесосинa', 'сучкa', 'проститутк', 'аутист', 'гандон', 'педик', 'мразь', 'тварь', 'гитлер', 'украин', 'росси', 'РФ', 'трахал', 'урод', 'хох', 'москал', 'свинорейх', 'рашист', 'укр-фашист', 'укрфашист', 'фашист', 'фашизм', 'фашик', 'путин', 'зеленский', 'зеленскому', 'зеленск']
channel_id = 1048513739558752276

class game_chat_warnings(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == channel_id and any(word in message.content.lower() for word in words):
            await message.reply('<@&1032200538516901899>\nСистема заметила сообщения которые возможно нарушают правила.')

async def setup(client):
    await client.add_cog(game_chat_warnings(client))
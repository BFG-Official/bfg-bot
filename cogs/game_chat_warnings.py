from discord.ext import commands

words = ['даун', 'долбaёб', 'долбаеб', 'нaхуй', 'даунихa', 'ебaл', 'шлюхa', 'пидор', 'пидорaс', 'негрилa', 'хуесос', 'хуесосинa', 'сучкa', 'проституткa', 'аутист', 'гандон', 'педик', 'мразь', 'тварь', 'гитлер', 'украина', 'украину', 'украины', 'россия', 'РФ', 'россию', 'россии', 'трахал', 'урод', 'хохол', 'хохлы', 'хохла', 'хохлов', 'москаль', 'москалей', 'москаля', 'свинорейх', 'рашист', 'укр-фашист', 'укрфашист', 'фашист', 'фашизм', 'фашиста', 'фашистов', 'фашик', 'фашиков', 'фашисты', 'фашики']
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
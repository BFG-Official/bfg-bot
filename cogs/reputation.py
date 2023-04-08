import discord
from discord.ext import commands
import asyncio, sqlite3

connection = sqlite3.connect('server.db')
cursor = connection.cursor()
first_time_rep = 60 * 3
third_time_rep = 60 * 60 * 3
second_time_rep = 60 * 60 * 12

async def first_rep(user_id, time):
    await asyncio.sleep(time)
    cursor.execute(f"UPDATE users SET first_rep = 1 WHERE id = {user_id}")
    connection.commit()

async def second_rep(user_id, time):
    await asyncio.sleep(time)
    cursor.execute(f"UPDATE users SET reps = 3 WHERE id = {user_id}")
    connection.commit()

async def third_rep(message_author_id, user_id, time):
    users_ids = cursor.execute(f"SELECT old_rep_user_id FROM users WHERE id = {message_author_id}").fetchone()[0]
    await asyncio.sleep(time)
    if str(user_id) in cursor.execute(f"SELECT old_rep_user_id FROM users WHERE id = {message_author_id}").fetchone()[0]:
        cursor.execute(f"UPDATE users SET old_rep_user_id = '{str(users_ids).replace(f'|{str(user_id)}|','')}' WHERE id = {message_author_id}")

allowed_users = [695684705328169060, 617415875947003915]

class reputation(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message = await commands.Bot.get_channel(self.client, payload.channel_id).fetch_message(payload.message_id)
        user = commands.Bot.get_channel(self.client, payload.channel_id).guild.get_member(payload.user_id)
        if message.author.bot: return
        if user.bot: return
        if message.author.id == user.id: return
        dm_channel = await user.create_dm()
        cursor.execute(f"UPDATE users SET is_bot_remove_react = 0 WHERE id = {user.id}")
        connection.commit()
        if payload.emoji.name in ['plusrep','minusrep']:
            if int(cursor.execute(f"SELECT first_rep FROM users WHERE id = {user.id}").fetchone()[0]) == 1 and int(cursor.execute(f"SELECT reps FROM users WHERE id = {user.id}").fetchone()[0]) > 0 and not (str(user.id) in str(cursor.execute(f"SELECT old_rep_user_id FROM users WHERE id = {message.author.id}").fetchone()[0])):
                if payload.emoji.name == 'plusrep':
                    cursor.execute(f"UPDATE users SET rep = rep + 1 WHERE id = {message.author.id}")
                    connection.commit()
                    rep = cursor.execute(f"SELECT rep FROM users WHERE id = {message.author.id}").fetchone()[0]
                    await commands.Bot.get_channel(self.client, 1082613972617936926).send(embed = discord.Embed(
                        description = f'Репутация участника __**{message.author}**__ повышена до __**{rep}**__ | `+1` | **[Сообщение](https://discord.com/channels/{payload.guild_id}/{payload.channel_id}/{payload.message_id})**\n\n**Содержание сообщения:** {message.content}',
                        color = discord.Colour.green()
                    ))
                elif payload.emoji.name == 'minusrep':
                    cursor.execute(f"UPDATE users SET rep = rep - 1 WHERE id = {message.author.id}")
                    connection.commit()
                    rep = cursor.execute(f"SELECT rep FROM users WHERE id = {message.author.id}").fetchone()[0]
                    await commands.Bot.get_channel(self.client, 1082613972617936926).send(embed = discord.Embed(
                        description = f'Репутация участника __**{message.author}**__ понижена до __**{rep}**__ | `-1` | **[Сообщение](https://discord.com/channels/{payload.guild_id}/{payload.channel_id}/{payload.message_id})**\n\n**Содержание сообщения:** {message.content}',
                        color = discord.Colour.red()
                    ))
                cursor.execute(f"UPDATE users SET first_rep = 0 WHERE id = {user.id}")
                old_users_ids = cursor.execute(f'SELECT old_rep_user_id FROM users WHERE id = {message.author.id}').fetchone()[0]
                cursor.execute(f"UPDATE users SET old_rep_user_id = '{str(old_users_ids) + f'|{str(user.id)}|'}' WHERE id = {message.author.id}")
                connection.commit()
                if int(cursor.execute(f"SELECT reps FROM users WHERE id = {user.id}").fetchone()[0]) == 3:
                    cursor.execute(f"UPDATE users SET reps = reps - 1 WHERE id = {user.id}")
                    connection.commit()
                    await first_rep(user.id, first_time_rep)
                    await third_rep(message.author.id, user.id, third_time_rep - first_time_rep)
                    await second_rep(user.id, second_time_rep - third_time_rep - first_time_rep)
                    return
                cursor.execute(f"UPDATE users SET reps = reps - 1 WHERE id = {user.id}")
                connection.commit()
                await first_rep(user.id, first_time_rep)
                await third_rep(message.author.id, user.id, third_time_rep - first_time_rep)
            elif int(cursor.execute(f"SELECT first_rep FROM users WHERE id = {user.id}").fetchone()[0]) == 0:
                cursor.execute(f"UPDATE users SET is_bot_remove_react = 1 WHERE id = {user.id}")
                connection.commit()
                if payload.emoji.name == 'plusrep': await message.remove_reaction('<:plusrep:1083761863696851094>', user)
                if payload.emoji.name == 'minusrep': await message.remove_reaction('<:minusrep:1083761892155203625>', user)
                await dm_channel.send(embed = discord.Embed(
                    description = 'Вы можете ставить репутационнную реакцию раз в __**3 минуты**__',
                    color = discord.Colour.random()
                ))
                cursor.execute(f"UPDATE users SET is_bot_remove_react = 0 WHERE id = {user.id}")
                connection.commit()
            elif str(user.id) in str(cursor.execute(f"SELECT old_rep_user_id FROM users WHERE id = {message.author.id}").fetchone()[0]):
                cursor.execute(f"UPDATE users SET is_bot_remove_react = 1 WHERE id = {user.id}")
                connection.commit()
                if payload.emoji.name == 'plusrep': await message.remove_reaction('<:plusrep:1083761863696851094>', user)
                if payload.emoji.name == 'minusrep': await message.remove_reaction('<:minusrep:1083761892155203625>', user)
                await dm_channel.send(embed = discord.Embed(
                    description = 'Вы можете ставить репутационню реакцию __**на одного участника**__ раз в __**3 часа**__',
                    color = discord.Colour.random()
                ))
                cursor.execute(f"UPDATE users SET is_bot_remove_react = 0 WHERE id = {user.id}")
                connection.commit()
            elif int(cursor.execute(f"SELECT reps FROM users WHERE id = {user.id}").fetchone()[0]) == 0:
                cursor.execute(f"UPDATE users SET is_bot_remove_react = 1 WHERE id = {user.id}")
                connection.commit()
                if payload.emoji.name == 'plusrep': await message.remove_reaction('<:plusrep:1083761863696851094>', user)
                if payload.emoji.name == 'minusrep': await message.remove_reaction('<:minusrep:1083761892155203625>', user)
                await dm_channel.send(embed = discord.Embed(
                    description = 'Ваше количество репутационных реакций __**закончилось**__, они восстановятся через __**12 часов**__',
                    color = discord.Colour.random()
                ))
                cursor.execute(f"UPDATE users SET is_bot_remove_react = 0 WHERE id = {user.id}")
                connection.commit()


        
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message = await commands.Bot.get_channel(self.client, payload.channel_id).fetch_message(payload.message_id)
        user = commands.Bot.get_channel(self.client, payload.channel_id).guild.get_member(payload.user_id)
        if message.author.bot: return
        if user.bot: return
        if message.author.id == user.id: return
        if payload.emoji.name == 'plusrep':
            if int(cursor.execute("SELECT is_bot_remove_react FROM users WHERE id = {}".format(user.id)).fetchone()[0]) == 0:
                cursor.execute(f"UPDATE users SET rep = rep - 1 WHERE id = {message.author.id}")
                connection.commit()
                rep = cursor.execute(f"SELECT rep FROM users WHERE id = {message.author.id}").fetchone()[0]
                await commands.Bot.get_channel(self.client, 1082613972617936926).send(embed = discord.Embed(
                    description = f'Репутация участника __**{message.author}**__ понижена до __**{rep}**__ | `-1` | **[Сообщение](https://discord.com/channels/{payload.guild_id}/{payload.channel_id}/{payload.message_id})**\n\n**Содержание сообщения:** {message.content}',
                    color = discord.Colour.red()
                ))
        elif payload.emoji.name == 'minusrep':
            if int(cursor.execute("SELECT is_bot_remove_react FROM users WHERE id = {}".format(user.id)).fetchone()[0]) == 0:
                cursor.execute(f"UPDATE users SET rep = rep + 1 WHERE id = {message.author.id}")
                connection.commit()
                rep = cursor.execute(f"SELECT rep FROM users WHERE id = {message.author.id}").fetchone()[0]
                await commands.Bot.get_channel(self.client, 1082613972617936926).send(embed = discord.Embed(
                    description = f'Репутация участника __**{message.author}**__ повышена до __**{rep}**__ | `+1` | **[Сообщение](https://discord.com/channels/{payload.guild_id}/{payload.channel_id}/{payload.message_id})**\n\n**Содержание сообщения:** {message.content}',
                    color = discord.Colour.green()
                ))


async def setup(client):
    await client.add_cog(reputation(client))
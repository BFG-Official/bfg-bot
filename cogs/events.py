import discord
from discord.ext import commands
import pytz, datetime, asyncio, sqlite3

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

class Events(commands.Cog):

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
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in [1048466435556515890, 1048513739558752276]: return
        if message.author.bot: return
        mess = message.content.lower()
        mess = ' ' + mess.replace('||','').replace('*','').replace('_','').replace('-','').replace('.','').replace('!','').replace('?','').replace('"','').replace("'","").replace('`','').replace('⠀','') + ' '
        for p in ['п','П','π','p','P','n']:
            for o in ['о','О','o','O','0','ο']:
                for n in ['н','Н','n','N','H','H']:
                    if (' ' + p + o + n + ' ' in mess):
                        await message.reply('пидораст ты', mention_author=True)
    
    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        if payload.channel_id in [1048466435556515890, 1048513739558752276]: return
        message = await commands.Bot.get_channel(self.client, payload.channel_id).fetch_message(payload.message_id)
        mess = payload.data['content']
        mess = ' ' + mess.replace('||','').replace('*','').replace('_','').replace('-','').replace('.','').replace('!','').replace('?','').replace('"','').replace("'","").replace('`','').replace('⠀','') + ' '
        for p in ['п','П','π','p','P','n']:
            for o in ['о','О','o','O','0','ο']:
                for n in ['н','Н','n','N','H']:
                    if (' ' + p + o + n + ' ' in mess):
                        await message.reply('пидораст ты', mention_author=True)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.bot: return
        async for log in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
            if log.target == member and log.user.bot:
                return

        roles_str = ''
        for role in member.roles:
            if role.name != '@everyone':
                roles_str += f'<@&{role.id}>\n'

        date_format = "%d.%m.%Y %H:%M:%S"

        join_date_str = member.joined_at.strftime(date_format) if member.joined_at else 'неизвестно'
        leave_date_str = datetime.datetime.now().strftime(date_format)

        channel = commands.Bot.get_channel(self.client, 1056222809057132635)

        embed = discord.Embed(
            title='**Участник покинул сервер!**',
            description=f'Дискорд тег человека: `{member}`\nДата входа на сервер: `{join_date_str}`\nДата выхода из сервера: `{leave_date_str}`',
            color=discord.Colour.red()
        )

        embed.add_field(name='ID', value=f'{member.id}')
        embed.add_field(name='Роли которые были при выходе', value=f'{roles_str}', inline=False)

        await channel.send(f'<@{member.id}> покинул сервер', embed = embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot: return
        timezone = pytz.timezone("Europe/Moscow")
        time_now = datetime.datetime.now(timezone)

        days = 7

        account_created_date = member.created_at
        days_since_creation = (time_now - account_created_date).days
        
        send_channel = commands.Bot.get_channel(self.client, 1056222809057132635)

        if days_since_creation < days:
            dm_channel = await member.create_dm()
            
            await dm_channel.send("Мы заметили, что вашему аккаунту меньше 7 дней, поэтому вам необходимо немного подождать, прежде чем присоединяться к нашему серверу.\n\nЭто связано с частыми случаями обхода блокировки на нашем сервере, если вы добропорядочный пользователь, то вам придется подождать 7 дней.\n\nЗа дополнительной информацией отпишите в Telegram: `@saberkovich`")

            embed = discord.Embed(
                title='**Участник был кикнут из-за малого возраста аккаунта!**',
                description=f'Дискорд тег человека: `{member}`\nID человека: `{member.id}`',
                color=discord.Colour.red()
            )

            await send_channel.send(embed = embed)
            print(f'\n\nКикнут с сервера:\n{member}\n\n')
            await asyncio.sleep(2)
            await member.kick(reason="Недостаточный возраст аккаунта")

        if days_since_creation > days:
            # Сообщение о входе
            created_at = member.created_at.strftime("%d.%m.%Y %H:%M:%S") if member.created_at else 'неизвестно'

            embed = discord.Embed(
                title = '**Участник присоединился к серверу**',
                description= f'Дискорд тег человека: `{member}`\nАккаунт создан: `{created_at}`',
                color = discord.Colour.green()
            )
            embed.add_field(name='ID', value=f'{member.id}')
            await send_channel.send(f'<@{member.id}> зашёл на сервер', embed = embed)

            welcome_embed = discord.Embed(
                title = 'Добро пожаловать на сервер!',
                description='Добро пожаловать на сервер **BFG Game Developer**!\n\nВсю нужную вам информацию можно прочитать в канале <#864854156842106910>, так же если имеются вопросы то вы можете спросить их в канале <#1047097724710944809>а.\n\n(Так же подписывайтесь на наш Telegram канал: https://t.me/teleportal_news)',
                color = discord.Colour.green()
            )
            welcome_embed.set_footer(text='Желаем удачи')

            dm_channel = await member.create_dm()
            await dm_channel.send(f'<@{member.id}>,', embed = welcome_embed)
            # Создание данных о пользователе
            if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES({member.id}, 0, 3, 1, 1, '{'|0|'}', 0, 0, 0)")
                connection.commit()
            else:
                pass

async def setup(client):
    await client.add_cog(Events(client))
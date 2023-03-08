import discord
from discord.ext import commands
from threading import Timer
import pytz, datetime, asyncio, sqlite3

connection = sqlite3.connect('server.db')
cursor = connection.cursor()
first_time_rep = 60 * 3
second_time_rep = 60 * 60 * 12
third_time_rep = 60 * 60 * 3

async def first_rep(user_id):
    cursor.execute("UPDATE users SET first_rep = 0 WHERE id = {}".format(user_id))
    connection.commit()
    await asyncio.sleep(first_time_rep)
    cursor.execute("UPDATE users SET first_rep = 1 WHERE id = {}".format(user_id))
    connection.commit()

async def second_rep(user_id):
    cursor.execute("UPDATE users SET reps = reps - 1 WHERE id = {}".format(user_id))
    connection.commit()
    await first_rep(user_id)
    await asyncio.sleep(second_time_rep - first_time_rep)
    cursor.execute("UPDATE users SET reps = 3 WHERE id = {}".format(user_id))
    connection.commit()

async def third_rep(user_id, message_author_id):
    cursor.execute("UPDATE users SET old_rep_message_author_id = {} WHERE id = {}".format(message_author_id, user_id))
    connection.commit()
    await first_rep(user_id)
    await asyncio.sleep(third_time_rep - first_time_rep)
    if int(cursor.execute("SELECT old_rep_message_author_id FROM users WHERE id = {}".format(user_id)).fetchone()[0]) == message_author_id:
        cursor.execute("UPDATE users SET old_rep_message_author_id = 0 WHERE id = {}".format(user_id))
        connection.commit()

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    '''@commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message = await commands.Bot.get_channel(self.client, payload.channel_id).fetch_message(payload.message_id)
        user = commands.Bot.get_channel(self.client, payload.channel_id).guild.get_member(payload.user_id)
        if message.author.bot: return
        if user.bot: return
        if message.author.id == user.id: return
        dm_channel = await user.create_dm()
        cursor.execute("UPDATE users SET is_bot_remove_react = 0 WHERE id = {}".format(user.id))
        connection.commit()
        if payload.emoji.name in ['mark_yes','mark_no']:
            if int(cursor.execute("SELECT first_rep FROM users WHERE id = {}".format(user.id)).fetchone()[0]) == 0 or int(cursor.execute("SELECT reps FROM users WHERE id = {}".format(user.id)).fetchone()[0]) == 0 or int(cursor.execute("SELECT old_rep_message_author_id FROM users WHERE id = {}".format(user.id)).fetchone()[0]) == message.author.id:
                cursor.execute("UPDATE users SET is_bot_remove_react = 1 WHERE id = {}".format(user.id))
                connection.commit()
                if payload.emoji.name == 'mark_no': await message.remove_reaction('<:mark_no:864461655407329322>', user)
                if payload.emoji.name == 'mark_yes': await message.remove_reaction('<:mark_yes:864461637000101909>', user)
                cursor.execute("UPDATE users SET is_bot_remove_react = 0 WHERE id = {}".format(user.id))
                connection.commit()
                if int(cursor.execute("SELECT reps FROM users WHERE id = {}".format(user.id)).fetchone()[0]) == 0:
                    await dm_channel.send(embed=discord.Embed(
                        description = 'Ваше количество репутационных реакций __**закончилось**__. Оно обновится через __**12 часов**__ после проставления первой реакции.',
                        color = discord.Colour.random()
                    ))
                    return
                if int(cursor.execute("SELECT first_rep FROM users WHERE id = {}".format(user.id)).fetchone()[0]) == 0:
                    await dm_channel.send(embed=discord.Embed(
                        description = 'Вы можете ставить репутационную реакцию раз в __**3 минуты**__.',
                        color = discord.Colour.random()
                    ))
                    return
                if int(cursor.execute("SELECT old_rep_message_author_id FROM users WHERE id = {}".format(user.id)).fetchone()[0]) == message.author.id:
                    await dm_channel.send(embed=discord.Embed(
                        description = 'Вы можете ставить репутационную реакцию на одного и того же человека раз в __**3 часа**__.',
                        color = discord.Colour.random()
                    ))
                    return
            if int(cursor.execute("SELECT first_rep FROM users WHERE id = {}".format(user.id)).fetchone()[0]) == 1:
                if payload.emoji.name == 'mark_yes':
                    cursor.execute("UPDATE users SET rep = rep + 1 WHERE id = {}".format(message.author.id))
                    await commands.Bot.get_channel(self.client, 1082613972617936926).send(embed=discord.Embed(
                        description = f'Репутация участника __**{message.author}**__ повышена до __**{int(cursor.execute("SELECT rep FROM users WHERE id = {}".format(message.author.id)).fetchone()[0])}**__ | `+1`',
                        color = discord.Colour.green()
                    ))
                elif payload.emoji.name == 'mark_no':
                    cursor.execute("UPDATE users SET rep = rep - 1 WHERE id = {}".format(message.author.id))
                    await commands.Bot.get_channel(self.client, 1082613972617936926).send(embed=discord.Embed(
                        description = f'Репутация участника __**{message.author}**__ понижена до __**{int(cursor.execute("SELECT rep FROM users WHERE id = {}".format(message.author.id)).fetchone()[0])}**__ | `-1`',
                        color = discord.Colour.red()
                    ))
                if int(cursor.execute("SELECT reps FROM users WHERE id = {}".format(user.id)).fetchone()[0]) == 3:
                    await second_rep(user.id)
                    return
                if int(cursor.execute("SELECT old_rep_message_author_id FROM users WHERE id = {}".format(user.id)).fetchone()[0]) != message.author.id:
                    await third_rep(user.id, message.author.id)
                    return
                cursor.execute("UPDATE users SET reps = reps - 1 WHERE id = {}".format(user.id))
                connection.commit()
                await first_rep(user.id)'''

        
    '''@commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message = await commands.Bot.get_channel(self.client, payload.channel_id).fetch_message(payload.message_id)
        user = commands.Bot.get_channel(self.client, payload.channel_id).guild.get_member(payload.user_id)
        if message.author.bot: return
        if user.bot: return
        if message.author.id == user.id: return
        if payload.emoji.name == 'mark_yes':
            if int(cursor.execute("SELECT is_bot_remove_react FROM users WHERE id = {}".format(user.id)).fetchone()[0]) == 1: return
            cursor.execute("UPDATE users SET rep = rep - 1 WHERE id = {}".format(message.author.id))
            await commands.Bot.get_channel(self.client, 1082613972617936926).send(embed=discord.Embed(
                description = f'Репутация участника __**{message.author}**__ понижена до __**{int(cursor.execute("SELECT rep FROM users WHERE id = {}".format(message.author.id)).fetchone()[0])}**__ | `-1`',
                color = discord.Colour.red()
            ))
        elif payload.emoji.name == 'mark_no':
            if int(cursor.execute("SELECT is_bot_remove_react FROM users WHERE id = {}".format(user.id)).fetchone()[0]) == 1: return
            cursor.execute("UPDATE users SET rep = rep + 1 WHERE id = {}".format(message.author.id))
            await commands.Bot.get_channel(self.client, 1082613972617936926).send(embed=discord.Embed(
                description = f'Репутация участника __**{message.author}**__ повышена до __**{int(cursor.execute("SELECT rep FROM users WHERE id = {}".format(message.author.id)).fetchone()[0])}**__ | `+1`',
                color = discord.Colour.green()
            ))'''
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in [1048466435556515890, 1048513739558752276]: return
        if message.author.bot: return
        mess = message.content.lower()
        mess = ' ' + mess.replace('||','').replace('*','').replace('_','').replace('-','').replace('.','').replace('!','').replace('?','').replace('"','').replace("'","").replace('`','').replace('⠀','') + ' '
        for p in ['п','П','π','p','P']:
            for o in ['о','О','o','O','0','ο']:
                for n in ['н','Н','n','N','H','H']:
                    if (' ' + p + o + n + ' ' in mess):
                        await message.reply('пидораст ты', mention_author=True)
    
    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        if payload.channel_id in [1048466435556515890, 1048513739558752276]: return
        mess = payload.data['content']
        mess = ' ' + mess.replace('||','').replace('*','').replace('_','').replace('-','').replace('.','').replace('!','').replace('?','').replace('"','').replace("'","").replace('`','').replace('⠀','') + ' '
        for p in ['п','П','π','p','P']:
            for o in ['о','О','o','O','0','ο']:
                for n in ['н','Н','n','N','H']:
                    if (' ' + p + o + n + ' ' in mess):
                        await commands.Bot.get_channel(self.client, payload.channel_id).send('пидораст ты')
    
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
                cursor.execute(f"INSERT INTO users VALUES({member.id}, 0, 0, 0, 0)")
                connection.commit()
            else:
                pass

async def setup(client):
    await client.add_cog(Events(client))
import discord
from discord.ext import commands
import pytz, datetime, asyncio

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == commands.Bot.user: return
        mess = message.content.lower()
        mess = ' ' + mess.replace('||','').replace('*','').replace('_','').replace('-','').replace('.','').replace('!','').replace('?','').replace('"','').replace("'","").replace('`','').replace('⠀','') + ' '
        for p in ['п','П','π','p','P']:
            for o in ['о','О','o','O','0']:
                for n in ['н','Н','n','N','H','H']:
                    if (' ' + p + o + n + ' ' in mess):
                        await message.reply('пидораст ты', mention_author=True)
    
    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        mess = payload.data['content']
        mess = ' ' + mess.replace('||','').replace('*','').replace('_','').replace('-','').replace('.','').replace('!','').replace('?','').replace('"','').replace("'","").replace('`','').replace('⠀','') + ' '
        for p in ['п','П','π','p','P']:
            for o in ['о','О','o','O','0']:
                for n in ['н','Н','n','N','H']:
                    if (' ' + p + o + n + ' ' in mess):
                        await commands.Bot.get_channel(self.client, payload.channel_id).send('пидораст ты')
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
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

async def setup(client):
    await client.add_cog(Events(client))
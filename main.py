import discord
import asyncio
from discord.ext import commands
import pytz
import datetime

bot = commands.Bot(command_prefix='>', intents=discord.Intents.all())

@bot.event
async def on_ready():
    timezone = pytz.timezone("Europe/Moscow")
    time_now = datetime.datetime.now(timezone)

    time_str = time_now.strftime("%d.%m.%Y %H:%M:%S")

    await bot.get_channel(1077307732757057656).send(f"Запуск завершен успешно! Время в которое включился бот [МСК]: `{time_str}`")
    print('BFG-bot готов к работе!')

    await send_message_on_day('Tuesday', 'Привет, сегодня вторник.')

## Переменные1

allowed_users = [695684705328169060, 617415875947003915]
allowed_roles = [964807055980523520]
moderator_roles = [964807055980523520, 854993494107750402, 960495606596517931, 873268262555750471, 975329806520553503, 1050457595963523203]
mapchecker_role = [1068946458201575605]

## Ивенты

@bot.event
async def send_message_on_day(day_name, message):
    timezone = pytz.timezone("Europe/Moscow")

    time_now = datetime.datetime.now(timezone)

    if time_now.strftime("%A") == day_name and time_now.hour == 18:
        channel = bot.get_channel(1066794825971679282)
        await channel.send(message)

@bot.event
async def on_member_remove(member):
  roles_str = ''
  for role in member.roles:
      if role.name != '@everyone':
          roles_str += f'<@&{role.id}>\n'

  date_format = "%d.%m.%Y %H:%M:%S"

  join_date_str = member.joined_at.strftime(date_format) if member.joined_at else 'неизвестно'
  leave_date_str = datetime.datetime.now().strftime(date_format)

  channel = bot.get_channel(1056222809057132635)

  embed = discord.Embed(
    title='**Участник покинул сервер!**',
    description=f'Дискорд тег человека: `{member}`\nID человека: `{member.id}`\nДата входа на сервер: `{join_date_str}`\nДата выхода из сервера: `{leave_date_str}`',
    color=000000
  )

  embed.add_field(name='Роли которые были при выходе', value=f'{roles_str}', inline=False)

  await channel.send(embed = embed)

## Команды

@bot.command()
async def привет(ctx):
  await ctx.send(f'Ну здарова, {ctx.message.author.mention}!')

@bot.command()
async def повтори(ctx, *, arg):
  await ctx.send(arg)

@bot.command()
async def очистить(ctx, count):
  try:
    count = int(count)
  except:
    await ctx.send('+очистить (число)')
    return
  try:
    if ctx.message.author.guild_permissions.administrator:
      if count > 0 and count <= 100:
        await ctx.channel.purge(limit=count+1)
      else:
        await ctx.send('Количество сообщений разрешено не менее 1 и не более 100.')
    else:
      await ctx.send('Вам нельзя использовать эту команду!')
  except:
    await ctx.send('Кажется я не могу удалять сообщения')
    return

@bot.command()
async def напомни(ctx, ttime, *, text = 'None'):
  if ctx.author.id in allowed_users:
    try:
      n = ttime + '+0300'
      a = datetime.datetime.strptime(n, '%d.%m.%Y_%H:%M%z')
      t = datetime.datetime.now(pytz.timezone("Europe/Moscow"))
      sa = a.timestamp()
      st = t.timestamp()
      time = int(sa) - int(st)
      if time > 0:
        message = await ctx.reply('Напоминание сработает <t:' + str(int(sa)) + ':R>')
        edit = 'Напоминание сработало <t:' + str(int(sa)) + ':R>'
        while time != 0:
          time -= 1
          print(time,text)
          await asyncio.sleep(1)
        if text == 'None':
          await message.edit(content = edit)
          await ctx.reply('Напоминание без текста')
        else:
          await message.edit(content = edit)
          await ctx.reply(ctx.message.author.mention + ', ' + text)
      else:
        await ctx.send('Пишите **будущую московскую** дату')
    except:
          await ctx.send('Пиши `+ждём (ДД.ММ.ГГ_ЧЧ:ММ) (текст)`. Писать **будущую московскую** дату')
  else:
    await ctx.send('Вам нельзя.')

@bot.command()
async def стартуй(ctx, count :int):
  if ctx.author.id in allowed_users:
    n = 0
    while n < count:
      n += 1
      await ctx.send(n)

## Тест команды

@bot.command()
async def тестэмбед(ctx):
  roles_str = ''
  for role in ctx.author.roles:
      if role.name != '@everyone':
          roles_str += f'<@&{role.id}>\n'
  
  embed = discord.Embed(
    title='**Ембед**',
    description='2 + 2 * 2',
    color=000000
  )

  embed.add_field(name='Ваши роли', value=f'{roles_str}', inline=False)

  await ctx.send(embed = embed)

## Запуск бота

bot.run('MTA3NzIzMzUzMTMyNDk5NzY3Mg.GqgPxz.X6Vw46JT6gifRMny4s3L_Jd6G4xYB-gTMjflNs')
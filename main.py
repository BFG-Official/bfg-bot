import discord
import asyncio
from discord.ext import commands
import pytz
import datetime

bot = commands.Bot(command_prefix='>', intents=discord.Intents.all())

@bot.event
async def on_ready():
  print('BFG-bot готов к работе!')

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
  if ctx.author.id in [695684705328169060, 617415875947003915]:
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
  if ctx.author.id in [695684705328169060, 617415875947003915]:
    n = 0
    while n < count:
      n += 1
      await ctx.send(n)

 ## Запуск бота

bot.run('MTA3NzIzMzUzMTMyNDk5NzY3Mg.GqgPxz.X6Vw46JT6gifRMny4s3L_Jd6G4xYB-gTMjflNs')
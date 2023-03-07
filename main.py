import discord
from discord.ext import commands
import pytz, datetime, asyncio

bot = commands.Bot(command_prefix='>', intents=discord.Intents.all())
bot.remove_command('help')

allowed_users = [695684705328169060, 617415875947003915]

cogs = ['admin','base','events','test']

@bot.event
async def on_ready():
    # Загрузка команд
    for extension in cogs:
        await bot.load_extension(f'cogs.{extension}')
        print(extension)
    # Запуск бота
    timezone = pytz.timezone("Europe/Moscow")
    time_now = datetime.datetime.now(timezone)

    time_str = time_now.strftime("%d.%m.%Y %H:%M:%S")

    # await bot.change_presence(activity=discord.Game(name="Включаюсь..."))
    await bot.get_channel(1077307732757057656).send(f"Запуск завершен успешно! Время в которое включился бот [МСК]: `{time_str}`")
    print('BFG-bot готов к работе!')
    # start_time = datetime.datetime.now()

    while True:
        # await bot.change_presence(activity=discord.Game(name=f"Аптайм: {str(datetime.datetime.now() - start_time).split('.')[0]}"))

        '''if datetime.datetime.now(timezone).strftime('%A_%H_%M_%S') == 'Saturday_20_00_00':
            await bot.get_channel(854994534391218176).send('<@783836872924987422>, <@940246956649873428>, <@711122945619263539>, <@874847454959378494>, <@1035626825277263902>, <@926917101355171852>, <@1027971828548903032>\Скидываем карту.')
        if datetime.datetime.now(timezone).strftime('%A_%H_%M_%S') == 'Sunday_10_00_00':
            await bot.get_channel(854994534391218176).send('тест')'''
            
        await asyncio.sleep(1)

bot.run('MTA3NzIzMzUzMTMyNDk5NzY3Mg.GqgPxz.X6Vw46JT6gifRMny4s3L_Jd6G4xYB-gTMjflNs')
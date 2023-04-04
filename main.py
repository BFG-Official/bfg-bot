import discord
from discord.ext import commands
import pytz, datetime, asyncio, sqlite3

bot = commands.Bot(command_prefix='>', intents=discord.Intents.all())
bot.remove_command('help')

allowed_users = [695684705328169060, 617415875947003915]

cogs = ['admin','base','events','test']

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

@bot.event
async def on_ready():
    # Проверка пользователей
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INT,
        rep BIGINT,
        reps INT,
        first_rep INT,
        second_rep INT,
        old_rep_user_id TEXT,
        is_bot_remove_react INT,
        lvl INT,
        exp_lvl INT
    )""")

    for guild in bot.guilds:
        for member in guild.members:
            if member.bot: pass
            if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES({member.id}, 0, 3, 1, 1, '{'|0|'}', 0, 0, 0)")
            else:
                pass
    connection.commit()
    cursor.execute("UPDATE users SET reps = 3")
    cursor.execute("UPDATE users SET first_rep = 1")
    cursor.execute("UPDATE users SET second_rep = 1")
    cursor.execute(f"UPDATE users SET old_rep_user_id = '{'|0|'}'")
    cursor.execute("UPDATE users SET is_bot_remove_react = 0")
    connection.commit()

    print('База данных подключена')

    # Загрузка команд
    for extension in cogs:
        await bot.load_extension(f'cogs.{extension}')
        print('Модуль',extension, 'подключён')
        await bot.get_channel(1077307732757057656).send(f'Модуль {extension} подключён')
    # Запуск бота
    timezone = pytz.timezone("Europe/Moscow")
    time_now = datetime.datetime.now(timezone)

    time_str = time_now.strftime("%d.%m.%Y %H:%M:%S")

    # await bot.change_presence(activity=discord.Game(name="Включаюсь..."))
    await bot.change_presence(activity=discord.Game(name="Напишите >хелп чтобы открыть список команд"))
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
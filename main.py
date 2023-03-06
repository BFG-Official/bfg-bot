import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix='>', intents=discord.Intents.all())
bot.remove_command('help')

allowed_users = [695684705328169060, 617415875947003915]

@bot.command
async def load(ctx, extension):
  if ctx.author.id in allowed_users:
    bot.load_extension(f"cogs.{extension}")
    await ctx.send("Cogs is loaded...")
  else:
    await ctx.send('Вы не резраб')

@bot.command
async def unload(ctx, extension):
  if ctx.author.id in allowed_users:
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send("Cogs is unloaded...")
  else:
    await ctx.send('Вы не резраб')

@bot.command
async def reload(ctx, extension):
  if ctx.author.id in allowed_users:
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    await ctx.send("Cogs is reloaded...")
  else:
    await ctx.send('Вы не резраб')

for filename in os.listdir("./cogs"):
  if filename.endswith(".py"):
    bot.load_extension(f"cogs.{filename[:-3]}")

bot.run('MTA3NzIzMzUzMTMyNDk5NzY3Mg.GqgPxz.X6Vw46JT6gifRMny4s3L_Jd6G4xYB-gTMjflNs')
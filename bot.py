import discord
from discord.ext import commands
import os
import json

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='[', intents=intents)

@bot.event
async def on_ready():
    await load_extensions()
    print('>> schwi bot is online <<')

@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'Loaded {extension} done.')

@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'Un - Loaded {extension} done.')

@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'Re - Loaded {extension} done.')

async def load_extensions():
    for filename in os.listdir('./cmds'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cmds.{filename[:-3]}')

if __name__ == '__main__':
    bot.run(jdata['TOKEN'])
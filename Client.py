import discord
import os
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    help_command=None,
    intents=intents
)


async def change_status():
    while True:
        try:
            await bot.change_presence(activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="über euch alle",
                state=discord.Status.online))
            await asyncio.sleep(60)
            await bot.change_presence(activity=discord.Game("$help"))
        except Exception as e:
            print(e)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    bot.loop.create_task(change_status())


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == "hi":
        await message.channel.send('Sup!')
    await bot.process_commands(message)


@bot.command()
async def ping(ctx):
    await ctx.reply(f'Pong! {round(bot.latency * 1000)}ms.')

bot.run(token)

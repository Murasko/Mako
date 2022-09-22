from distutils.cmd import Command
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    print(f'Bot {client.user} logged in!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.lower() == "hi":
        await message.channel.send('Sup!')

    if "käsekuchen" in message.content.lower():
        await message.channel.send('Beste Kuchen!')

client.run(token)
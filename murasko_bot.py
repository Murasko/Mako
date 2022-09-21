import discord
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

muraskoBot = discord.Client(intents=intents)

@muraskoBot.event
async def on_ready():
    print(f'Bot {muraskoBot.user} logged in!')

@muraskoBot.event
async def on_message(message):
    if message.author == muraskoBot.user:
        return
    
    if message.content.lower() == "hi":
        await message.channel.send('Sup!')

muraskoBot.run(token)
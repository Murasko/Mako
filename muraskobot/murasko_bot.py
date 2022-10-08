import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')

class MuraskoBot(discord.Client):
    async def on_ready(self):
        print(f'Bot {self.user} logged in!')
    
    async def on_message(self, message):
        if message.author == self.user:
            return
    
        if message.content.lower() == "hi":
            await message.channel.send('Sup!')

        if "käsekuchen" in message.content.lower():
            await message.channel.send('Beste Kuchen!')

intents = discord.Intents.default()
intents.message_content = True

MuraskoBot = MuraskoBot(intents=intents)
MuraskoBot.run(token)
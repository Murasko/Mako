import asyncio
import json
import logging
import os

import discord

with open("config.json") as config_file:
    config = json.load(config_file)

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename="discord.log",
    encoding="utf-8",
    mode="w")

handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

intents = discord.Intents.all()

bot = discord.Bot(intents=intents)


async def change_status():
    try:
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="über euch alle",
                state=discord.Status.online,
            )
        )
        print("Status set!")
    except Exception as e:
        print(e)


async def load_cogs():
    for file in os.listdir("./src/cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"src.cogs.{extension}")
                print(f"Loaded Extension {extension}")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await change_status()

if __name__ == "__main__":
    asyncio.run(load_cogs())
    bot.run(config["discord_token"])

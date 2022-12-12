import asyncio
import json
import logging
import os
import platform
import sys

import aiosqlite
import discord

if not os.path.isfile("config.json"):
    sys.exit("Couldn't find 'config.json'! Please make sure you've added it.")
else:
    with open("config.json") as config_file:
        config = json.load(config_file)

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

intents = discord.Intents.all()

bot = discord.Bot(intents=intents)

bot.config = config


async def init_database() -> None:
    async with aiosqlite.connect("mako/db/database.db") as database:
        with open("mako/db/schema.sql") as database_schema:
            await database.executescript(database_schema.read())
        await database.commit()


@bot.event
async def on_ready() -> None:
    print()
    print(f"Logged in as {bot.user}")
    print(f"discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    await change_discord_status()
    print()


async def change_discord_status() -> None:
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="über euch alle",
            state=discord.Status.online,
        )
    )
    print("Status set!")


async def load_cogs() -> None:
    for file in os.listdir("mako/cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"mako.cogs.{extension}")
                print(f"Loaded Extension {extension}")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


if __name__ == "__main__":
    asyncio.run(init_database())
    asyncio.run(load_cogs())
    bot.run(config["discord_token"])

#  Mako - Python Discord Bot
#  Copyright (c) 2023. Marco Murawski
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  Contact:
#  info@murasko.de
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  Contact:
#  info@murasko.de

import discord
from tortoise import Tortoise, run_async

import json
import logging
import os
import platform
import sys

from mako.db import User, Guild

if not os.path.isfile("config.json"):
    sys.exit("Couldn't find 'config.json'! Please make sure you've added it.")
else:
    with open("config.json") as config_file:
        config = json.load(config_file)

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="../discord.log", encoding="utf-8", mode="w")

handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

intents = discord.Intents.all()

bot = discord.Bot(intents=intents)

bot.config = config


async def init_database() -> None:
    await Tortoise.init(db_url='sqlite://db/db.sqlite3', modules={'models': ['db.models']})
    await Tortoise.generate_schemas()
    print('Initialized Database')


def load_cogs() -> None:
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"mako.cogs.{extension}")
                print(f"Loaded Extension {extension}")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


# load_cogs()
bot.load_extension('mako.cogs.orm')


@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user}")
    print(f"py-cord API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print()
    await change_discord_status()
    print()


async def change_discord_status() -> None:
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="über diesen Server",
            state=discord.Status.online,
        )
    )
    print("Status set!")


if __name__ == "__main__":
    bot.loop.create_task(init_database())
    bot.run(config["discord_token"])

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

import discord
from tortoise import Tortoise, run_async

import json
import logging
import os
import platform
import sys

from mako.db.models import Guild, DiscordUser

if not os.path.isfile("config.json"):
    sys.exit("Couldn't find 'config.json'! Please make sure you've added it.")
else:
    with open("config.json") as config_file:
        config = json.load(config_file)

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="logs/discord.log", encoding="utf-8", mode="w")

handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

intents = discord.Intents.all()

bot = discord.Bot(intents=intents)

bot.config = config


async def init_database() -> None:
    await Tortoise.init(
        db_url="sqlite://mako/db/db.sqlite3", modules={"models": ["mako.db.models"]}
    )
    await Tortoise.generate_schemas()
    print("Initialized Database")


async def guild_init() -> None:
    for current_guild in bot.guilds:
        if not current_guild.system_channel:
            notification_channel = 0
        else:
            notification_channel = current_guild.system_channel.id
        if not await Guild.filter(id=current_guild.id).exists():
            owner_id = current_guild.owner.id
            if not await DiscordUser.filter(id=current_guild.owner.id).exists():
                guild, _ = await Guild.get_or_create(
                    id=current_guild.id,
                    notification_channel=notification_channel,
                    owner=owner_id,
                )
            else:
                guild, _ = await Guild.get_or_create(
                    id=current_guild.id,
                    notification_channel=notification_channel,
                    owner=owner_id,
                )
            print(
                f"Added {owner_id} / {str(current_guild.owner)} as Owner for "
                f"{guild.id} / {current_guild.name} to Database."
            )
        else:
            continue
    print("Initialized Guilds Table")


def load_cogs(cog_dir="mako/cogs", log_file="logs/cog_load.log") -> None:
    logging.basicConfig(filename=log_file, level=logging.INFO)
    for file in os.listdir(cog_dir):
        if file.endswith(".py") and not file.startswith("__"):
            extension = file[:-3]
            try:
                bot.load_extension(f"mako.cogs.{extension}")
                logging.info(f"Loaded Extension {extension}")
            except (ImportError, SyntaxError) as e:
                logging.error(
                    f"Failed to load extension {extension}\n{type(e).__name__}: {e}"
                )
            except Exception as e:
                logging.error(
                    f"Failed to load extension {extension}\n{type(e).__name__}: {e}",
                    exc_info=True,
                )


load_cogs()


async def change_discord_status() -> None:
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="über diesen Server",
            state=discord.Status.online,
        )
    )
    print("Status set")


@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user}")
    print(f"py-cord API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print()
    await change_discord_status()
    print()
    await guild_init()


if __name__ == "__main__":
    run_async(init_database())
    bot.run(config["discord_token"])

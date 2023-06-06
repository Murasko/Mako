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
from tortoise import Tortoise
from dotenv import dotenv_values

import asyncio
import logging
import os
import platform
import sys

from src.mako.db.models import DiscordGuild, DiscordUser

if not os.path.isfile(".env"):
    sys.exit("Couldn't find '.env'! Please make sure you've created it.")
else:
    config = dotenv_values(".env")

logger = logging.getLogger("discord")
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename="mako.log", encoding="utf-8", mode="w")

handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

intents = discord.Intents.all()


class Mako(discord.Bot):
    async def close(self) -> None:
        await Tortoise.close_connections()
        await super().close()

    async def on_ready(self) -> None:
        print(f"Logged in as {bot.user}")
        print(f"py-cord API version: {discord.__version__}")
        print(f"Python version: {platform.python_version()}")
        print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        print()
        await change_discord_status()
        print()
        await guild_init()
        print()


bot = Mako(intents=intents)

bot.config = config


async def init_database() -> None:
    await Tortoise.init(
        db_url="sqlite://mako/db/db.sqlite3", modules={"models": ["src.mako.db.models"]}
    )
    await Tortoise.generate_schemas(safe=True)
    print("Database startup done")


async def guild_init() -> None:
    for current_guild in bot.guilds:
        if not current_guild.system_channel:
            notification_channel = 0
        else:
            notification_channel = current_guild.system_channel.id
        if not await DiscordGuild.filter(id=current_guild.id).exists():
            owner_id = current_guild.owner.id
            if not await DiscordUser.filter(user_id=current_guild.owner.id).exists():
                guild, _ = await DiscordGuild.get_or_create(
                    id=current_guild.id,
                    notification_channel=notification_channel,
                    owner=owner_id,
                )
            else:
                guild, _ = await DiscordGuild.get_or_create(
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
    print("Guild init done")


def load_cogs(cog_dir="mako/cogs") -> None:
    for file in os.listdir(cog_dir):
        if file.endswith(".py") and not file.startswith("__"):
            extension = file[:-3]
            try:
                bot.load_extension(f"src.mako.cogs.{extension}")
                logger.info(f"Loaded Extension {extension}")
            except (ImportError, SyntaxError) as e:
                logger.error(
                    f"Failed to load extension {extension}\n{type(e).__name__}: {e}"
                )
            except Exception as e:
                logger.error(
                    f"Failed to load extension {extension}\n{type(e).__name__}: {e}",
                    exc_info=True,
                )
    print("Loaded Cogs")


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


if __name__ == "__main__":
    asyncio.run(init_database())
    bot.run(config["DISCORD_TOKEN"])

from src.twitch import get_notifications, get_profile_pictures

import logging
import os
from dotenv import load_dotenv

import discord
from discord.ext import tasks

load_dotenv()
token = os.environ["TOKEN"]

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

cogs_list = [
    'greetings',
    'utils',
    'music'
]

intents = discord.Intents.all()

mako = discord.Bot(intents=intents)


async def change_status():
    try:
        await mako.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="über euch alle",
                state=discord.Status.online,
            )
        )
        print("Status set!")
    except Exception as e:
        print(e)


@tasks.loop(minutes=5)
async def check_twitch_online():
    try:
        channel = mako.get_channel(int(os.getenv("NOTIFY_CHANNEL")))
        if not channel:
            return

        notifications = get_notifications()
        for notification in notifications:
            embed = discord.Embed(
                title="{} ist Live".format(notification["user_name"]),
                colour=discord.Colour.random(),
            )
            embed.set_author(name="Mako")
            embed.set_thumbnail(url=get_profile_pictures(notification["user_id"]))
            embed.add_field(name="Titel: ", value=notification["title"])
            embed.add_field(name="Spielt: ", value=notification["game_name"])

            await channel.send(embed=embed)
    except Exception as e:
        print(e)


@mako.event
async def on_ready():
    print(f"Logged in as {mako.user}")
    await change_status()
    await check_twitch_online.start()


if __name__ == "__main__":
    for cog in cogs_list:
        mako.load_extension(f"src.cogs.{cog}")
        print(f"Loaded Cog {cog}")

    mako.run(token)

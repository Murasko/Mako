"""
TODO:
- Get a few commands Up and running
- Rolesystem based on Commands or Reactions, maybe Dropdowns
- Remove Intents.all and set only needed Intents and Persmissions for Bot User

Optional:
- Implement Setup Wizard
- Research and implement cogs
"""
import logging
import os
import asyncio
from dotenv import load_dotenv

import discord
from discord.ext import tasks

from twitch import get_notifications, get_profile_pictures

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.all()

bot = discord.Bot(intents=intents)


async def change_status():
    try:
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="über euch alle",
            state=discord.Status.online))
    except Exception as e:
        print(e)


@tasks.loop(minutes=5)
async def check_twitch_online():
    while True:
        try:
            channel = bot.get_channel(1029147523593551942)
            if not channel:
                return

            notifications = get_notifications()
            for notification in notifications:
                embed = discord.Embed(title="{} ist Live".format(
                    notification["user_name"]), colour=discord.Colour.random())
                embed.set_author(name="MuraskoBot")
                embed.set_thumbnail(
                    url=get_profile_pictures(notification["user_id"]))
                embed.add_field(name="Titel: ", value=notification["title"])
                embed.add_field(name="Spielt: ",
                                value=notification["game_name"])

                await channel.send(embed=embed)
        except Exception as e:
            print(e)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await change_status()
    check_twitch_online.start()


@bot.event
async def on_member_join(member):
    system_channel = member.guild.system_channel
    await system_channel.send(
        f"Hallo {member.mention}, schön das du hier bist.")


@bot.slash_command()
async def ping(ctx):
    await ctx.respond(f"Pong! {round(bot.latency * 1000)}ms.")


@bot.slash_command()
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    pfp = member.display_avatar
    roles = []
    for i in member.roles:
        if i.name == "@everyone":
            pass
        else:
            roles.append(str(i.name))

    embed = discord.Embed(
        title=f'Userinformation für {member}', colour=discord.Colour.random())
    embed.set_thumbnail(url=pfp)
    embed.add_field(name="Joined Server: ",
                    value=member.joined_at.strftime("%d/%m/%Y"))
    embed.add_field(name="Joined Discord: ",
                    value=member.created_at.strftime("%d/%m/%Y"))
    embed.add_field(name="Roles: ", value=str(roles), inline=False)

    await ctx.respond(embed=embed)


if __name__ == "__main__":
    bot.run(token)

"""
TODO:
- Get a few commands Up and running
- Implement Twitch Live Messages
- Rolesystem based on Commands or Reactions

Optional:
- Implement Setup Wizard
- Research and implement cogs
"""
import discord

import os
import asyncio
import random

from dotenv import load_dotenv

from twitch import get_notifications, get_profile_pictures

load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.all()

bot = discord.Bot(intents=intents)


async def change_status():
    while True:
        try:
            await bot.change_presence(activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="über euch alle",
                state=discord.Status.online))
            await asyncio.sleep(60)
            await bot.change_presence(activity=discord.Game("$help"))
        except Exception as e:
            print(e)


async def check_twitch_online():
    while True:
        try:
            channel = bot.get_channel(1029034984767500298)
            if not channel:
                return

            notifications = get_notifications()
            for notification in notifications:
                embed = discord.Embed(title="{} ist Live".format(notification["user_name"]),
                                      colour=discord.Colour.random())
                embed.set_author(name="MuraskoBot")
                embed.set_thumbnail(url=get_profile_pictures(notification["user_id"]))
                embed.add_field(name="Titel: ", value=notification["title"])
                embed.add_field(name="Spielt: ", value=notification["game_name"])
                embed.add_field(name="Aktuelle Zuschauer: ", value=notification["viewer_count"], inline=False)

                await channel.send(embed=embed)
            await asyncio.sleep(20)
        except Exception as e:
            print(e)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    bot.loop.create_task(change_status())
    bot.loop.create_task(check_twitch_online())


@bot.event
async def on_member_join(member):
    system_channel = member.guild.system_channel
    await system_channel.send(f'Hallo {member.mention}, schön das du hier bist.')


@bot.slash_command()
async def ping(ctx):
    await ctx.respond(f'Pong! {round(bot.latency * 1000)}ms.')


@bot.slash_command()
async def eightball(ctx, *, question):
    answers = ["Na sicher doch", "Was denkst du wer du bist"]
    await ctx.respond(f'**Frage: ** {question}\n **Antwort: ** {random.choice(answers)}')


@bot.slash_command()
async def userinfo(ctx, member):
    # TODO: Implement Userinfo without Params for Command Caller

    pfp = member.display_avatar

    roles = []
    for i in member.roles:
        if i.name == "@everyone":
            pass
        else:
            roles.append(str(i.name))

    embed = discord.Embed(title=f'Userinformation für {member}', colour=discord.Colour.random())
    embed.set_thumbnail(url=pfp)
    embed.add_field(name="Joined Server: ", value=member.joined_at.strftime("%d/%m/%Y"))
    embed.add_field(name="Joined Discord: ", value=member.created_at.strftime("%d/%m/%Y"))
    embed.add_field(name="Roles: ", value=str(roles), inline=False)

    await ctx.respond(embed=embed)


if __name__ == "__main__":
    bot.run(token)

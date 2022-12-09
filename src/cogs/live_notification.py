import json

from src.twitch import get_notifications, get_profile_picture

import discord
from discord.ext import commands, tasks

with open("config.json") as config_file:
    config = json.load(config_file)


class LiveNotifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(minutes=5)
    async def check_twitch_online(self, bot):
        try:
            channel = bot.get_channel(int(config["notification_channel"]))
            if not channel:
                raise Exception("Notification Channel nicht vorhanden")

            notifications = get_notifications()
            for notification in notifications:
                embed = discord.Embed(
                    title="{} ist Live".format(notification["user_name"]),
                    colour=discord.Colour.random()
                )
                embed.set_author(name="Mako")
                embed.set_thumbnail(url=get_profile_picture(notification["user_id"]))
                embed.add_field(name="Titel: ", value=notification["title"])
                embed.add_field(name="Spielt: ", value=notification["game_name"])

                await channel.send(embed=embed)
        except Exception as e:
            print(e)

    @commands.slash_command()
    async def refresh_notifications(self, ctx):
        await ctx.respond("Erneuere Notifications.")
        await self.check_twitch_online(self.bot)


def setup(bot):
    bot.add_cog(LiveNotifications(bot))

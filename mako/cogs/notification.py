import asyncio

import discord
from discord.ext import commands
from twitchAPI.twitch import Twitch


class TwitchNotification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notification_sent = []

    async def send_notification_when_live(self) -> None:
        notification_channel = self.bot.get_channel(
            int(self.bot.config["notification_channel"])
        )
        twitch = Twitch(
            self.bot.config["twitch_client_id"], self.bot.config["twitch_client_secret"]
        )
        streams = twitch.get_streams(user_login=self.bot.config["watchlist"])
        async for stream in streams:
            if stream.type == "live":
                embed = discord.Embed(
                    title=f"{stream.user_login} ist Live",
                    colour=discord.Colour.random(),
                )
                embed.set_author(name="Mako")
                # embed.set_thumbnail(url=self.get_twitch_profile_picture(notification["user_id"]))
                embed.add_field(name="Titel: ", value=stream.title)
                embed.add_field(name="Spielt: ", value=stream.game_name)

                await notification_channel.send(embed=embed)

    @commands.slash_command()
    async def trigger_notifications(self, ctx) -> None:
        await self.send_notification_when_live()
        await ctx.respond("Noti")


def setup(bot):
    bot.add_cog(TwitchNotification(bot))

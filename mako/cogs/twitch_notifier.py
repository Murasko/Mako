#  Mako - Multipurpose python bot
#  Copyright (c) 2022. Marco Murawski
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
import time

import discord
from discord.ext import commands, tasks
from twitchAPI.twitch import Twitch

from mako.db import database_manager


class TwitchNotification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.save_user_profile_pictures.start()
        self.notification_sent = []
        self.send_notification_when_live.start()

    @discord.slash_command()
    async def reload_twitch_notifier(self, ctx):
        self.bot.reload_extension('mako.cogs.twitch_notifier')
        await ctx.respond('Reloaded Twitch Notifier.')

    @tasks.loop(hours=48)
    async def save_user_profile_pictures(self) -> None:
        twitch = await Twitch(self.bot.config["twitch_client_id"], self.bot.config["twitch_client_secret"])
        users = twitch.get_users(logins=self.bot.config["watchlist"])

        async for user in users:
            profile_image_url = user.profile_image_url
            print(user.login, profile_image_url)
            profile_image_list = await database_manager.get_saved_profile_images(user.login)
            if profile_image_list is None:
                await database_manager.save_twitch_user_profile_picture(user.login, profile_image_url)

    @tasks.loop(minutes=5)
    async def send_notification_when_live(self) -> None:
        currently_live = []
        notification_channel = self.bot.get_channel(
            int(self.bot.config["notification_channel"])
        )
        twitch = await Twitch(
            self.bot.config["twitch_client_id"], self.bot.config["twitch_client_secret"]
        )
        streams = twitch.get_streams(user_login=self.bot.config["watchlist"])
        async for stream in streams:
            currently_live.append(stream.user_login)
            if stream.user_login not in self.notification_sent:
                profile_image_url = await database_manager.get_saved_profile_images(
                    stream.user_login
                )
                embed = discord.Embed(
                    title=f"{stream.user_login} ist Live",
                    colour=discord.Colour.random(),
                    url=f"https://www.twitch.tv/{stream.user_login}",
                )
                embed.set_author(name="Mako")
                embed.set_thumbnail(url=profile_image_url[1])
                embed.add_field(name="Titel: ", value=stream.title)
                embed.add_field(name="Spielt: ", value=stream.game_name)

                await notification_channel.send(embed=embed)
                self.notification_sent.append(stream.user_login)

        for user in self.bot.config["watchlist"]:
            is_live = True
            if user not in currently_live:
                is_live = False
            if user in self.notification_sent and not is_live:
                self.notification_sent.remove(user)


def setup(bot):
    bot.add_cog(TwitchNotification(bot))

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
from discord.ext import commands, tasks
from twitchAPI.twitch import Twitch

from src.mako.db.models import DiscordGuild
from src.mako.db.models import Watchlist
from src.mako.utils.checks import is_admin


class TwitchNotification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.save_user_profile_pictures.start()
        # self.send_notification_when_live.start()

    @is_admin()
    @discord.slash_command()
    async def reload_twitch_notifier(self, ctx):
        self.bot.reload_extension("mako.cogs.twitch_notifier")
        await ctx.respond("Reloaded Twitch Notifier.")

    # @tasks.loop(hours=48)
    # async def save_user_profile_pictures(self) -> None:
    #     twitch = await Twitch(
    #         self.bot.config["TWITCH_CLIENT_ID"], self.bot.config["TWITCH_CLIENT_SECRET"]
    #     )
    #     for uid in Watchlist.id:
    #         user = await Watchlist.get(id=uid)
    #         profile_picture_url = user.twitch_profile_picture_url
    #
    # @tasks.loop(seconds=10)
    # async def send_notification_when_live(self) -> None:
    #     twitch = await Twitch(
    #         self.bot.config["TWITCH_CLIENT_ID"], self.bot.config["TWITCH_CLIENT_SECRET"]
    #     )
    #     for guild in self.bot.guilds:
    #         notification_channel = await database_manager.get_notification_channel(
    #             int(guild.id)
    #         )
    #         if not notification_channel:
    #             continue
    #         else:
    #             watchlist = await database_manager.get_watchlist(int(guild.id))
    #             if not watchlist:
    #                 continue
    #             else:
    #                 partial_notification_channel = self.bot.get_partial_messageable(
    #                     notification_channel
    #                 )
    #                 streams = twitch.get_streams(
    #                     stream_type="live", user_login=watchlist
    #                 )
    #                 async for stream in streams:
    #                     # Überprüfe den Stream-Status und sende die Benachrichtigung nur, wenn er offline ist
    #                     current_status = await get_streamer_status(stream.user_login)
    #                     if current_status != "live":
    #                         # Update the streamer status in the database to 'live'
    #                         await update_streamer_status(stream.user_login, "live")
    #                         # Send notification
    #                         profile_image_url = (
    #                             await database_manager.get_saved_profile_images(
    #                                 stream.user_login
    #                             )
    #                         )
    #                         embed = discord.Embed(
    #                             title=f"{stream.user_login} ist Live",
    #                             colour=discord.Colour.random(),
    #                             url=f"https://www.twitch.tv/{stream.user_login}",
    #                         )
    #                         embed.set_author(name="Mako")
    #                         embed.set_thumbnail(url=profile_image_url)
    #                         embed.add_field(name="Titel: ", value=stream.title)
    #                         embed.add_field(name="Spielt: ", value=stream.game_name)
    #                         await partial_notification_channel.send(embed=embed)
    #
    # @discord.slash_command(
    #     guild_only=True, guild_ids=[656899959035133972, 1054741800671252532]
    # )
    # @is_admin()
    # async def add_watchlist(self, ctx, username: str) -> None:
    #     await ctx.respond(await database_manager.set_watchlist(ctx.guild.id, username))
    #     await self.save_user_profile_pictures()
    #
    # @discord.slash_command(
    #     guild_only=True, guild_ids=[656899959035133972, 1054741800671252532]
    # )
    # @is_admin()
    # async def get_watchlist(self, ctx) -> None:
    #     watchlist = await database_manager.get_watchlist(ctx.guild.id)
    #     await ctx.respond(
    #         f"The following Users are on the Watchlist on {ctx.guild}: {watchlist}"
    #     )
    #
    # @discord.slash_command(
    #     guild_only=True, guild_ids=[656899959035133972, 1054741800671252532]
    # )
    # @is_admin()
    # async def remove_watchlist(self, ctx, username: str) -> None:
    #     await ctx.respond(
    #         await database_manager.remove_watchlist(ctx.guild.id, username)
    #     )


def setup(bot):
    bot.add_cog(TwitchNotification(bot))

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
from twitchAPI.helper import first
from twitchAPI.twitch import Twitch

from datetime import datetime

from src.mako.db.models import TwitchUser, DiscordGuild, GuildTwitchUser
from src.mako.utils.checks import is_admin


class TwitchNotification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_user_profile_pictures.start()
        self.send_live_notification.start()

    @tasks.loop(hours=6)
    async def update_user_profile_pictures(self) -> None:
        for user in await TwitchUser.all():
            await self.save_profile_picture_url(user.username)

    async def save_profile_picture_url(self, username: str) -> None:
        twitch = await Twitch(
            self.bot.config["TWITCH_CLIENT_ID"], self.bot.config["TWITCH_CLIENT_SECRET"]
        )
        user = await first(twitch.get_users(logins=username))
        await TwitchUser.filter(username=username.lower()).update(
            profile_picture_url=user.profile_image_url
        )

    @tasks.loop(seconds=10)
    async def send_live_notification(self) -> None:
        twitch = await Twitch(
            self.bot.config["TWITCH_CLIENT_ID"], self.bot.config["TWITCH_CLIENT_SECRET"]
        )

        async for guild in DiscordGuild.exclude(
            notification_channel=0
        ).prefetch_related("twitch_users"):
            notification_channel = guild.notification_channel
            partial_notification_channel = self.bot.get_partial_messageable(
                notification_channel
            )
            guild_twitch_users = await guild.twitch_users.all()

            for guild_twitch_user in guild_twitch_users:
                twitch_user = await TwitchUser.filter(
                    pk=guild_twitch_user.twitch_user_id
                ).first()
                streams = twitch.get_streams(
                    user_login=twitch_user.username, stream_type="live"
                )
                async for stream in streams:
                    if (
                        guild_twitch_user.last_notification_time is None
                        or stream.started_at > guild_twitch_user.last_notification_time
                    ):
                        embed = discord.Embed(
                            title=f"{stream.user_login} ist Live",
                            colour=discord.Colour.random(),
                            url=f"https://www.twitch.tv/{stream.user_login}",
                        )
                        embed.set_author(name="Mako")
                        embed.set_thumbnail(url=twitch_user.profile_picture_url)
                        embed.add_field(name="Titel: ", value=stream.title)
                        embed.add_field(name="Spielt: ", value=stream.game_name)
                        embed.set_image(
                            url=stream.thumbnail_url.replace("{width}", "960").replace(
                                "{height}", "675"
                            )
                        )
                        current_time = datetime.now().astimezone()
                        guild_twitch_user.last_notification_time = current_time
                        await guild_twitch_user.save()
                        await partial_notification_channel.send(embed=embed)

    @is_admin()
    @discord.slash_command(
        guild_only=True, guild_ids=[656899959035133972, 1054741800671252532]
    )
    async def add_watchlist(self, ctx, username: str) -> None:
        if await GuildTwitchUser.filter(
            guild=ctx.author.guild.id, twitch_user=username.lower()
        ).exists():
            await ctx.respond(
                f"User {username} is already on the watchlist for this guild."
            )
        else:
            twitch_user, _ = await TwitchUser.get_or_create(username=username.lower())
            await GuildTwitchUser(
                guild_id=ctx.author.guild.id, twitch_user=twitch_user
            ).save()
            await self.save_profile_picture_url(username.lower())
            await ctx.respond(f"Added {username.lower()} to watchlist.")

    @is_admin()
    @discord.slash_command(
        guild_only=True, guild_ids=[656899959035133972, 1054741800671252532]
    )
    async def get_watchlist(self, ctx) -> None:
        if await GuildTwitchUser.filter(guild=ctx.author.guild.id).exists():
            guild_watchlist = await GuildTwitchUser.filter(
                guild_id=ctx.author.guild.id
            ).prefetch_related("twitch_user")
            watchlist = [user.twitch_user.username for user in guild_watchlist]
            watchlist_output = "\n".join(watchlist)
            await ctx.respond(
                f"The following users are on the watchlist: \n{watchlist_output}"
            )
        else:
            await ctx.respond("No watchlist configured yet.")

    @is_admin()
    @discord.slash_command(
        guild_only=True, guild_ids=[656899959035133972, 1054741800671252532]
    )
    async def remove_watchlist(self, ctx, username: str) -> None:
        await GuildTwitchUser.filter(
            guild=ctx.author.guild.id, twitch_user=username.lower()
        ).delete()
        await ctx.respond(f"Removed {username.lower()} from the watchlist.")


def setup(bot):
    bot.add_cog(TwitchNotification(bot))

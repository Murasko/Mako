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

from tortoise import fields
from tortoise.models import Model


class DiscordGuild(Model):
    id = fields.BigIntField(pk=True)
    notification_channel = fields.BigIntField()
    owner = fields.BigIntField()
    admins = fields.ManyToManyField("models.DiscordUser", related_name="admins")


class DiscordUser(Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField()
    guilds = fields.ManyToManyField("models.DiscordGuild", related_name="members")


class TwitchUser(Model):
    username = fields.CharField(pk=True, max_length=100, unique=True)
    twitch_id = fields.CharField(max_length=100)


class Watchlist(Model):
    id = fields.IntField(pk=True)
    twitch_user = fields.ForeignKeyField("models.TwitchUser", related_name="watchlists")
    guild = fields.ForeignKeyField("models.DiscordGuild", related_name="watchlists")
    twitch_profile_picture_url = fields.CharField(max_length=200)


class NotificationHistory(Model):
    id = fields.IntField(pk=True)
    twitch_user = fields.ForeignKeyField(
        "models.TwitchUser", related_name="notifications"
    )
    guild_id = fields.BigIntField()
    last_notification = fields.DatetimeField()

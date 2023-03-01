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


class Guild(Model):
    id = fields.BigIntField(pk=True)
    notification_channel = fields.BigIntField()
    owner = fields.BigIntField()
    admins = fields.ManyToManyField(
        "models.DiscordUser",
        related_name="admin_guilds",
        through="bot_admins",
        backward_key="guild_id",
    )


class DiscordUser(Model):
    id = fields.BigIntField(pk=True)
    guilds = fields.ManyToManyField("models.Guild", related_name="members")


class TwitchUser(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=100, unique=True)
    twitch_id = fields.CharField(max_length=100)


class Watchlist(Model):
    id = fields.IntField(pk=True)
    twitch_user = fields.ForeignKeyField("models.TwitchUser", related_name="watchlists")
    guild = fields.ForeignKeyField("models.Guild", related_name="watchlists")


class NotificationHistory(Model):
    id = fields.IntField(pk=True)
    twitch_user = fields.ForeignKeyField(
        "models.TwitchUser", related_name="notifications"
    )
    last_notification = fields.DatetimeField()


class BotAdmin(Model):
    user = fields.ForeignKeyField("models.DiscordUser", on_delete=fields.CASCADE)
    guild = fields.ForeignKeyField(
        "models.Guild",
        on_delete=fields.CASCADE,
        related_name="bot_admins",
    )

    class Meta:
        unique_together = ("user", "guild")

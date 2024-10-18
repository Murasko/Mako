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
    notification_channel = fields.BigIntField(null=True)
    owner = fields.BigIntField()
    admins: fields.ManyToManyRelation["DiscordUser"] = fields.ManyToManyField(
        "models.DiscordUser", related_name="admin_guilds"
    )
    users: fields.ManyToManyRelation["DiscordUser"] = fields.ManyToManyField(
        "models.DiscordUser", related_name="guilds"
    )
    twitch_users: fields.ReverseRelation["GuildTwitchUser"]


class DiscordUser(Model):
    user_id = fields.BigIntField(pk=True)
    admin_guild: fields.ManyToManyRelation["DiscordUser"]
    guilds: fields.ManyToManyRelation["DiscordUser"]


class TwitchUser(Model):
    username = fields.CharField(pk=True, max_length=100, unique=True)
    profile_picture_url = fields.CharField(max_length=200, null=True)
    guilds: fields.ReverseRelation["GuildTwitchUser"]


class GuildTwitchUser(Model):
    guild: fields.ForeignKeyRelation["DiscordGuild"] = fields.ForeignKeyField(
        "models.DiscordGuild", related_name="twitch_users"
    )
    twitch_user: fields.ForeignKeyRelation["TwitchUser"] = fields.ForeignKeyField(
        "models.TwitchUser", related_name="guilds"
    )
    last_notification_time = fields.DatetimeField(null=True)

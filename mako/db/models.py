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

from tortoise.models import Model
from tortoise import fields


class Guild(Model):
    id = fields.BigIntField(pk=True)
    notification_channel = fields.BigIntField()
    owner = fields.ForeignKeyField(
        model_name="models.User", related_name="owned_guilds"
    )
    admins = fields.ManyToManyField(
        model_name="models.User", related_name="administered_guilds"
    )


class DiscordUser(Model):
    id = fields.BigIntField(pk=True)
    owned_guilds: fields.ReverseRelation["Guild"]
    administered_guilds: fields.ManyToManyRelation["Guild"]


class Watchlist(Model):
    username = fields.CharField(pk=True, max_length=50)
    discord_guild = 
    notification_sent = 


class TwitchUser(Model):
    username = fields.CharField(pk=True, max_length=50)
    profile_picture_url = fields.CharField(max_length=500)
    status = fields.CharField(max_length=8, default="offline")
    
from tortoise import fields
from tortoise.models import Model


class TwitchUser(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=100, unique=True)
    twitch_id = fields.CharField(max_length=100)


class DiscordGuild(Model):
    id = fields.BigIntField(pk=True)
    admins = fields.ManyToManyField('models.DiscordUser', related_name='admin_of_guilds')


class DiscordUser(Model):
    id = fields.BigIntField(pk=True)
    is_bot_admin = fields.BooleanField(default=False)
    guilds = fields.ManyToManyField('models.DiscordGuild', related_name='members')


class Watchlist(Model):
    id = fields.IntField(pk=True)
    twitch_user = fields.ForeignKeyField('models.TwitchUser', related_name='watchlists')
    guild = fields.ForeignKeyField('models.DiscordGuild', related_name='watchlists')


class NotificationHistory(Model):
    id = fields.IntField(pk=True)
    twitch_user = fields.ForeignKeyField('models.TwitchUser', related_name='notifications')
    last_notification = fields.DatetimeField()


from tortoise.models import Model
from tortoise import fields


class TwitchUser(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=100)
    twitch_id = fields.CharField(max_length=30)


class DiscordGuild(Model):
    id = fields.IntField(pk=True)
    guild_id = fields.CharField(max_length=30, unique=True)
    notification_channel_id = fields.CharField(max_length=30)
    twitch_users = fields.ManyToManyField('models.TwitchUser', related_name='discord_guilds', through='watchlist')


class Watchlist(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.TwitchUser', related_name='watchlists')
    guild = fields.ForeignKeyField('models.DiscordGuild', related_name='watchlists')
    is_live = fields.BooleanField(default=False)
    last_notification = fields.DatetimeField(null=True)


class BotAdministrator(Model):
    id = fields.IntField(pk=True)
    user_id = fields.CharField(max_length=30, unique=True)
    guild = fields.ForeignKeyField('models.DiscordGuild', related_name='bot_administrators')


class ServerOwner(Model):
    id = fields.IntField(pk=True)
    user_id = fields.CharField(max_length=30, unique=True)
    guild = fields.ForeignKeyField('models.DiscordGuild', related_name='server_owner')


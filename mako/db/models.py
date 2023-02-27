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
    owner = fields.ForeignKeyField(model_name='models.User', related_name='owned_guilds')
    admins = fields.ManyToManyField(model_name='models.User', related_name='administered_guilds')
    watchlist = fields.ManyToManyField(model_name='models.Watchlist', related_name='watchlist')


class User(Model):
    id = fields.BigIntField(pk=True)
    owned_guilds: fields.ManyToManyRelation['Guild']
    administered_guilds: fields.ManyToManyRelation['Guild']


class Watchlist(Model):
    username = fields.CharField(pk=True, max_length=50)


class Notifications(Model):
    username = fields.CharField(pk=True, max_length=50)
    profile_picture_url = fields.CharField(max_length=500)
    status = fields.CharField(max_length=8, default='offline')

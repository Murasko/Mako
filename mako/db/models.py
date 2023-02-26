from tortoise.models import Model
from tortoise import fields


class Guild(Model):
    guild_id = fields.BigIntField(pk=True)
    notification_channel = fields.BigIntField()
    owner = fields.ForeignKeyField(model_name='mako.User', related_name='owner_id')
    admins = fields.ManyToManyField(model_name='mako.User', related_name='admin_id')
    twitch_watchlist = fields.ManyToManyField(model_name='mako.TwitchWatchlist', related_name='twitch_username')


class User(Model):
    user_id = fields.BigIntField(pk=True)


class TwitchWatchlist(Model):
    username = fields.CharField(max_length=50, pk=True)


class TwitchNotifications(Model):
    username = fields.CharField(max_length=100, pk=True)
    profile_picture_url = fields.CharField(max_length=500)
    status = fields.CharField(max_length=50, default='offline')

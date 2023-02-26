from tortoise.models import Model
from tortoise import fields


class Guild(Model):
    id = fields.BigIntField(pk=True)
    notification_channel = fields.BigIntField(null=True)
    owner = fields.ForeignKeyField(model_name='models.User', related_name='owned_guilds')
    admins = fields.ManyToManyField(model_name='models.User', related_name='administered_guilds')
    watchlist = fields.ManyToManyField(model_name='models.Watchlist', related_name='watchlist')


class User(Model):
    id = fields.BigIntField(pk=True)
    owned_guilds: fields.ManyToManyRelation['Guild']
    administered_guilds: fields.ManyToManyRelation['Guild']


class Watchlist(Model):
    username = fields.CharField(max_length=50)


class Notifications(Model):
    username = fields.CharField(pk=True, max_length=50)
    profile_picture_url = fields.CharField(max_length=500)
    status = fields.CharField(max_length=8, default='offline')

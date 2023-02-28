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

from discord.ext import commands
from tortoise import Tortoise

from mako.db import Guild


def is_owner():
    async def predicate(ctx):
        guild_id = ctx.author.guild.id
        owner_query = await Guild.filter(id=guild_id).values_list("owner_id")
        await Tortoise.close_connections()
        owner_id = owner_query[0][0]
        if ctx.author.id == owner_id:
            return True
        else:
            await ctx.respond("You need to be the Owner to use this command!")

    return commands.check(predicate)


def is_admin():
    async def predicate(ctx):
        owner_query = await Guild.filter(id=ctx.author.guild.id).values_list("owner_id")
        guild = await Guild.get(id=ctx.author.guild.id)
        admin_ids = [admin.id for admin in await guild.admins.all()]
        if ctx.author.id in owner_query[0] or admin_ids:
            print(admin_ids)
            return True
        else:
            await ctx.respond("You need to be an Admin to use this command!")

    return commands.check(predicate)

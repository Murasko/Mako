#  Mako - Python Discord Bot
#  Copyright (c) 2024. Marco Murawski
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

from mako.db.models import DiscordGuild


def is_owner():
    async def predicate(ctx):
        if ctx.author.id == ctx.guild.owner.id:
            return True
        else:
            await ctx.respond("You need to be the Owner to use this command!")

    return commands.check(predicate)


def is_admin():
    async def predicate(ctx):
        guild = await DiscordGuild.get(id=ctx.author.guild.id)
        admin_ids = [admin.user_id for admin in await guild.admins]
        if ctx.author.id in admin_ids or guild.owner:
            return True
        else:
            await ctx.respond("You need to be an Admin to use this command!")

    return commands.check(predicate)

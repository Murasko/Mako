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

from mako.db import database_manager


def is_admin():
    async def predicate(ctx):
        if str(ctx.author) in await database_manager.get_guild_administrator(ctx.guild.id):
            return True
        else:
            await ctx.respond('Du besitzt nicht die notwendigen Berechtigungen um diesen Command zu benutzen!')
    return commands.check(predicate)

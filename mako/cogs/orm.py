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

import discord
from discord.ext import commands
from tortoise import Tortoise

from mako.db import User, Guild


class Orm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def test(self):
        for current_guild in self.bot.guilds:
            if not await Guild.filter(guild_id=current_guild.id).exists():
                if not await User.filter(user_snowflake=current_guild.owner.id).exists():
                    owner = await User.get_or_create(user_snowflake=current_guild.owner.id)
                    guild = await Guild.get_or_create(guild_id=current_guild.id,
                                                      notification_channel=current_guild.system_channel.id,
                                                      owner=owner)
                else:
                    owner = await User.get_or_create(user_snowflake=current_guild.owner.id)
                    guild = await Guild.get_or_create(guild_id=current_guild.id,
                                                      notification_channel=current_guild.system_channel.id,
                                                      owner=owner)
                print(f'Saved {guild[0].id}/{current_guild.name} with owner '
                      f'{owner[0].id}/{str(current_guild.owner)} to Database.')
            else:
                continue
        await Tortoise.close_connections()

    @discord.slash_command(guild_only=True, guild_ids=[656899959035133972, 1054741800671252532])
    async def test_commands(self, ctx) -> None:
        await self.test()
        await ctx.respond('Done')


def setup(bot):
    bot.add_cog(Orm(bot))

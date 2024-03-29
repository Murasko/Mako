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

import discord
from discord.ext import commands


class Greetings(commands.Cog, name="greetings"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        await member.guild.system_channel.send(f"Hi {member.mention}, viel Spaß hier!")

    @commands.Cog.listener()
    async def on_member_leave(self, member: discord.Member) -> None:
        await member.guild.system_channel.send(f"{member.mention} verlässt uns leider.")


def setup(bot):
    bot.add_cog(Greetings(bot))

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


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def ping(self, ctx) -> None:
        await ctx.respond(f"Pong! {round(self.bot.latency * 1000)}ms.")

    @discord.slash_command()
    async def userinfo(self, ctx, member: discord.Member = None) -> None:
        if member is None:
            member = ctx.author

        user_avatar = member.display_avatar
        roles = []
        for role in member.roles:
            if role.name == "@everyone":
                pass
            else:
                roles.append(str(role.name))

        embed = discord.Embed(
            title=f"User-information für {member}", colour=discord.Colour.random()
        )
        embed.set_thumbnail(url=user_avatar)
        embed.add_field(
            name="Joined Server: ", value=member.joined_at.strftime("%d/%m/%Y")
        )
        embed.add_field(
            name="Joined Discord: ", value=member.created_at.strftime("%d/%m/%Y")
        )
        embed.add_field(name="Roles: ", value=str(roles), inline=False)

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Utils(bot))

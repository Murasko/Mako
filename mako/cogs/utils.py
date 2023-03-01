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

from mako.db.models import Guild, DiscordUser
from mako.utils.checks import is_owner, is_admin


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @is_admin()
    @discord.slash_command()
    async def reload_utils(self, ctx):
        self.bot.reload_extension("mako.cogs.utils")
        await ctx.respond("Reloaded Utils.")

    @discord.slash_command()
    async def ping(self, ctx) -> None:
        await ctx.respond(f"Pong! {round(self.bot.latency * 1000)}ms.")

    @discord.slash_command(guild_ony=True)
    async def userinfo(
        self,
        ctx,
        member: discord.Member = None,
    ) -> None:
        if member is None:
            member = ctx.author

        user_avatar = member.display_avatar
        roles = [role.name for role in member.roles]
        roles.remove("@everyone")

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
        embed.add_field(name="Roles: ", value=str(", ".join(roles)), inline=False)

        await ctx.respond(embed=embed)

    @is_admin()
    @discord.slash_command(
        guild_only=True, guild_ids=[656899959035133972, 1054741800671252532]
    )
    async def get_administrator(self, ctx) -> None:
        guild = await Guild.get(id=ctx.author.guild.id)
        admin_ids = [admin.id for admin in await guild.admins]
        admins = []
        for admin in admin_ids:
            user = self.bot.get_user(admin)
            admins.append(f"ID: {admin} / Name: {user.name}#{user.discriminator}")
        format_admins = "\n".join(admins)
        await ctx.respond(
            f"These users are currently admins on this guild:\n{format_admins}"
        )

    @is_owner()
    @discord.slash_command(
        guild_only=True, guild_ids=[656899959035133972, 1054741800671252532]
    )
    async def add_administrator(self, ctx, user_id) -> None:
        guild = await Guild.get(id=ctx.author.guild.id)
        user, _ = await DiscordUser.get_or_create(id=user_id)
        await guild.admins.add(user)
        await ctx.respond(f"Added {user_id} as admin.")

    @is_owner()
    @discord.slash_command(
        guild_only=True, guild_ids=[656899959035133972, 1054741800671252532]
    )
    async def remove_administrator(self, ctx, user_id) -> None:
        guild = await Guild.get(id=ctx.author.guild.id)
        user = await DiscordUser.get(id=user_id)
        await guild.admins.remove(user)
        await ctx.respond(f"Removed {user_id} as admin.")

    @is_admin()
    @discord.slash_command(
        guild_only=True, guild_ids=[656899959035133972, 1054741800671252532]
    )
    async def set_notification_channel(self, ctx, notification_channel_id):
        await Guild.filter(id=ctx.author.guild.id).update(
            notification_channel=notification_channel_id
        )
        await ctx.respond(
            f"Set channel with ID {notification_channel_id} as notification channel."
        )

    @is_admin()
    @discord.slash_command(
        guild_only=True, guild_ids=[656899959035133972, 1054741800671252532]
    )
    async def get_notification_channel(self, ctx):
        guild = await Guild.get(id=ctx.author.guild.id)
        channel = self.bot.get_channel(guild.notification_channel)
        await ctx.respond(
            f"Current notification channel: \nName: {channel} // ID: {channel.id}"
        )


def setup(bot):
    bot.add_cog(Utils(bot))

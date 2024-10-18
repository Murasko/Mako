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

from mako.db.models import DiscordGuild, DiscordUser
from mako.utils.checks import is_owner, is_admin


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    reload = discord.SlashCommandGroup("reload", "Commands to reload modules")
    tools = discord.SlashCommandGroup("utils", "Useful small tools")
    admins = discord.SlashCommandGroup("admins", "Manage Bot Administrators")
    notification_channel = discord.SlashCommandGroup(
        "notification_channel", "Manage the notification channel"
    )

    @is_admin()
    @reload.command(description="Reload the Greetings module")
    async def greetings(self, ctx):
        self.bot.reload_extension("mako.cogs.greetings")
        await ctx.respond("Reloaded Greetings.")

    @is_admin()
    @reload.command(description="Reload the Twitch module")
    async def twitch(self, ctx) -> None:
        self.bot.reload_extension("mako.cogs.twitch_notifier")
        await ctx.respond("Reloaded Twitch Notifier.")

    @is_admin()
    @reload.command(description="Reload the Utils module")
    async def utils(self, ctx):
        self.bot.reload_extension("mako.cogs.utils")
        await ctx.respond("Reloaded Utils.")

    @tools.command(description="Prints the Ping of the Bot")
    async def ping(self, ctx) -> None:
        await ctx.respond(f"{round(self.bot.latency * 1000)}ms.")

    @discord.user_command(name="Basic User Info", guild_ony=True)
    async def userinfo(
        self,
        ctx,
        member: discord.Member = None,
    ) -> None:
        user_avatar = member.display_avatar
        roles = [role.name for role in member.roles]
        roles.remove("@everyone")

        embed = discord.Embed(title=f" {member}", colour=discord.Colour.random())
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
    @admins.command(description="Print the current Bot Admins.")
    async def print(self, ctx) -> None:
        guild = await DiscordGuild.get(id=ctx.author.guild.id)
        admin_ids = [admin.user_id for admin in await guild.admins]
        admins = []
        for admin in admin_ids:
            user = self.bot.get_user(admin)
            admins.append(f"ID: {admin} / Name: {user.name}#{user.discriminator}")
        format_admins = "\n".join(admins)
        if not admins:
            await ctx.respond(f"There are currently no users added as admins.")
        else:
            await ctx.respond(
                f"These users are currently admins on this guild:\n{format_admins}"
            )

    @is_owner()
    @discord.user_command(name="Add Bot Admin")
    async def add_administrator(self, ctx, member: discord.member) -> None:
        guild = await DiscordGuild.get(id=ctx.author.guild.id)
        user, _ = await DiscordUser.get_or_create(user_id=member.id)
        await guild.admins.add(user)
        await ctx.respond(f"Added {member} to Bot Administrators.")

    @is_owner()
    @discord.user_command(name="Remove Bot Admin")
    async def remove_administrator(self, ctx, member: discord.member) -> None:
        guild = await DiscordGuild.get(id=ctx.author.guild.id)
        user = await DiscordUser.get(user_id=member.id)
        await guild.admins.remove(user)
        await ctx.respond(f"Removed {member} from Bot Administrators.")

    @is_admin()
    @notification_channel.command(
        description="Set the Notification Channel for this Guild."
    )
    async def set(self, ctx, notification_channel_id):
        await DiscordGuild.filter(id=ctx.author.guild.id).update(
            notification_channel=notification_channel_id
        )
        await ctx.respond(
            f"Set channel with ID {notification_channel_id} as notification channel."
        )

    @is_admin()
    @notification_channel.command(
        description="Print the Notification Channel for this Guild."
    )
    async def print(self, ctx):
        guild = await DiscordGuild.get(id=ctx.author.guild.id)
        channel = self.bot.get_channel(guild.notification_channel)
        await ctx.respond(
            f"Current notification channel: \nName: {channel} // ID: {channel.id}"
        )


def setup(bot):
    bot.add_cog(Utils(bot))

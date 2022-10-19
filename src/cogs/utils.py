import discord
from discord.ext import commands


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def ping(self, ctx):
        await ctx.respond(f"Pong! {round(self.latency * 1000)}ms.")

    @discord.slash_command()
    async def userinfo(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        pfp = member.display_avatar
        roles = []
        for i in member.roles:
            if i.name == "@everyone":
                pass
            else:
                roles.append(str(i.name))

        embed = discord.Embed(
            title=f"Userinformation für {member}", colour=discord.Colour.random()
        )
        embed.set_thumbnail(url=pfp)
        embed.add_field(name="Joined Server: ", value=member.joined_at.strftime("%d/%m/%Y"))
        embed.add_field(
            name="Joined Discord: ", value=member.created_at.strftime("%d/%m/%Y")
        )
        embed.add_field(name="Roles: ", value=str(roles), inline=False)

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Utils(bot))

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

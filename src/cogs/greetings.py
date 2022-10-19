import discord
from discord.ext import commands


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def goodbye(self, ctx):
        await ctx.respond('Goodbye!')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        system_channel = member.guild.system_channel
        await system_channel.send(f"Hi {member.mention}, viel Spaß hier!")


def setup(bot):
    bot.add_cog(Greetings(bot))

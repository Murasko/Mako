import discord
import os
import asyncio
import random
from dotenv import load_dotenv


load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.all()

bot = discord.Bot(intents=intents)


async def change_status():
    while True:
        try:
            await bot.change_presence(activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="über euch alle",
                state=discord.Status.online))
            await asyncio.sleep(60)
            await bot.change_presence(activity=discord.Game("$help"))
        except Exception as e:
            print(e)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    bot.loop.create_task(change_status())


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == "Hi".lower():
        await message.channel.send('Sup!')
    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    system_channel = member.guild.system_channel
    await system_channel.send(f'Hallo {member.mention}, schön das du hier bist.')


@bot.slash_command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms.')


@bot.slash_command(aliases=["muschel", "q"])
async def eightball(ctx, *, question):
    answers = ["Na sicher doch", "Was denkst du wer du bist"]
    await ctx.send(f'**Frage: ** {question}\n **Antwort: ** {random.choice(answers)}')


@bot.slash_command()
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    name = member.display_name
    pfp = member.display_avatar

    roles = []
    for i in member.roles:
        if i.name == "@everyone":
            pass
        else:
            roles.append(str(i.name))

    embed = discord.Embed(title=f'Userinformation für {name}', colour=discord.Colour.random())
    embed.set_thumbnail(url=pfp)
    embed.add_field(name="Joined Server: ", value=member.joined_at.strftime("%d/%m/%Y"))
    embed.add_field(name="Joined Discord: ", value=member.created_at.strftime("%d/%m/%Y"))
    embed.add_field(name="Roles: ", value=roles, inline=False)

    await ctx.send(embed=embed)

bot.run(token)

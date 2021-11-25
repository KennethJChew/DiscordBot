import os
import random
import discord
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands.core import cooldown
from discord.flags import Intents
from dotenv import load_dotenv
from discord.ext import commands
from cogs import Greetings
import help

# Bot setup
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
SERVER = os.getenv("DISCORD_SERVER")

attributes = {
    "name":"help11111",
    "aliases":["help","helps"],
    "cooldown":commands.Cooldown(1,10,commands.BucketType.user)
}
help_object = help.myHelp(command_attrs=attributes)
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!",help_command=help_object,intents = intents)
bot.add_cog(Greetings(bot))
print("Cog added!")


@bot.event
async def on_ready():
    print("{bot} has connected to Discord successfully and is ready!".format(bot=bot.user.name))
    # print(f"{bot.user.name} has connected to Discord!")

# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Command
@bot.command(help="Shows all bot's command usage in the server on a sorted list.",aliases=["br","brrr","botranks","botpos","botposition","botpositions"])
async def botrank(ctx,bot:discord.Member):
    pass

@bot.command(name="99",help="Responds with a random quote from Brooklyn 99")
# bot commands must accept at least 1 parameter called ctx which is the context
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name="google",help="Responds with a url to google")
async def google(ctx):
    google_url = "https://www.google.com"
    await ctx.send(google_url)




@bot.command(name="create-channel",help="Creates a channel")
# @commands.has_role("admin")
async def create_channel(ctx,a,b,c,channel_name="test channel"):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels,name=channel_name)
    if not existing_channel:
        print(f"Creating the new channel: {channel_name}")
        await guild.create_text_channel(channel_name)

# msg = None
# @bot.event
# async def on_message(message):
#     msg=message
#     await bot.get_context(message)
#     print("context acquired")

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.errors.CheckFailure):
        await ctx.send("You don't have the correct role to execute this command")
    if isinstance(error,commands.errors.CommandNotFound):
        await ctx.send("Invalid command entered")
        print("getting ctx")
        print(ctx.message)
        # await bot.get_context(ctx.message)
        print("got ctx")
    if isinstance(error,commands.errors.DiscordException):
        print(error)


# async def invalid_command(ctx):
#     print("Invalid command")
#     await bot.invoke("!help")

bot.run(TOKEN)
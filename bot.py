import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

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

@bot.command(name="create-channel")
@commands.has_role("admin")
async def create_channel(ctx,channel_name="test channel"):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels,name=channel_name)
    if not existing_channel:
        print(f"Creating the new channel: {channel_name}")
        await guild.create_text_channel(channel_name)

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.errors.CheckFailure):
        await ctx.send("You don't have the correct role to execute this command")


bot.run(TOKEN)
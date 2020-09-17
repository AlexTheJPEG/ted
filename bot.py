import json
import logging
import os
from itertools import cycle
from random import choice

import discord
from discord.ext import commands, tasks

# Set up logging
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

# Load settings from settings.json
settings = json.loads(open("settings.json", "r").read())

# Token and command prefix
token = settings["token"]
prefix = settings["prefix"]

# Respond to self / other bots
respond_to_self = settings["respond_to_self"]
respond_to_bots = settings["respond_to_bots"]


# Ready messages and status change messages
with open("ready_responses.txt") as file:
    _ready = [response.strip() for response in file.readlines()]
status = cycle([f"Try {prefix}help!", "with 1s and 0s"])

# Client initialization
client = commands.Bot(command_prefix=prefix)


# Start status changing loop and print ready message
@client.event
async def on_ready():
    change_status.start()
    print(choice(_ready))


# Erorr handling
@client.event
async def on_command_error(ctx, error):
    mention = ctx.author.mention
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            f"{mention} That's not a valid command! "
            f"Type `{prefix}help` for a list of commands."
        )
    elif isinstance(error, commands.errors.InvalidEndOfQuotedStringError):
        await ctx.send(
            f"{mention} Make sure your entire question is in quotes "
            "and there's nothing after the quotes!"
        )
    elif isinstance(error, commands.errors.ExpectedClosingQuoteError):
        await ctx.send(
            f"{mention} I only see the starting quote..."
            "are you sure you put an ending quote?"
        )


# Message handling
@client.event
async def on_message(message):
    # Make sure bot doesn't respond to itself
    if message.author.id == client.user.id and respond_to_self == "False":
        return

    # Make sure bot doesn't respond to other bots
    if message.author.bot and respond_to_bots == "False":
        return

    await client.process_commands(message)


# Change status from trying the help message to a funny message
@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


# Load cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

# Run the bot
client.run(token)

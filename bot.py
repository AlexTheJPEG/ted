import discord
import json
import logging
import os
from discord.ext import commands, tasks
from random import choice
from itertools import cycle

# Set up logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8',
                              mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Load settings from settings.json
settings = json.loads(open('settings.json', 'r').read())

# Token and command prefix
_token = settings['token']
_prefix = settings['prefix']
_respond_to_self = settings['respond_to_self']
_respond_to_bots = settings['respond_to_bots']

# Client initialization
client = commands.Bot(command_prefix=_prefix)

# Ready messages and status change messages
with open("ready_responses.txt") as file:
    _ready = [response.strip() for response in file.readlines()]
_status = cycle([f"Try {_prefix}help!", "with 1s and 0s"])

# Start status changing loop and print ready message
@client.event
async def on_ready():
    change_status.start()
    print(choice(_ready))

# Erorr handling
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"That's not a valid command! Type `{_prefix}help` for a list of commands.")
    elif isinstance(error, commands.errors.InvalidEndOfQuotedStringError):
        await ctx.send("Make sure your entire question is in quotes and there's nothing after the quotes!")
    elif isinstance(error, commands.errors.ExpectedClosingQuoteError):
        await ctx.send("I only see the starting quote...are you sure you put an ending quote?")


# Change status from trying the help message to a funny message
@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(_status)))

# Load cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

# Run the bot
client.run(_token)

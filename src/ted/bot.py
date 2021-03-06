import json
import logging
import os
from itertools import cycle
from secrets import choice

import discord
from discord import Intents
from discord.ext import commands, tasks

from ted import __version__

# Set up logging
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)


def read_json(path):
    with open(path, "r") as json_file:
        data = json.load(json_file)
    return data


def write_json(data, path):
    with open(path, "w") as json_file:
        json.dump(data, json_file, indent=2)


class Bot(commands.Bot):
    def __init__(self):
        # Load settings from settings.json
        self.settings = read_json("./settings.json")

        # Token and command prefix
        self.token = self.settings["token"]
        self.prefix = self.settings["prefix"]

        # Blacklisted users
        self.blacklisted = self.settings["blacklisted"]

        # Ready messages and status change messages
        with open("./ready_responses.txt") as file:
            self.ready = [response.strip() for response in file.readlines()]
        self.status = cycle([f"Try {self.prefix}help!", "with 1s and 0s"])

        # Intent initialization
        intents = Intents.default()

        # Client initialization
        super().__init__(command_prefix=self.prefix, intents=intents)

    def run(self, version):
        # Set the version
        self.version = version

        # Run the bot
        super().run(self.token, reconnect=True)

    async def on_ready(self):
        # Load cogs
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"cogs.{filename[:-3]}")

        # Start changing the status
        self.change_status.start()

        # Print ready message
        print(choice(self.ready))

    async def on_message(self, message):
        # Make sure bot doesn't respond to itself or other bots
        if message.author.id == self.user.id or message.author.bot:
            return

        # Make sure bot doesn't respond to blacklisted users
        if message.author.id in self.blacklisted:
            return

        # Process the message for commands
        await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        mention = ctx.author.mention

        # Ignore these errors
        ignored = (commands.CommandNotFound, commands.UserInputError)
        if isinstance(error, ignored):
            return

        # Handle string quotation errors
        if isinstance(error, commands.errors.InvalidEndOfQuotedStringError):
            await ctx.send(
                f"{mention} Make sure your entire question is in quotes "
                "and there's nothing after the quotes!"
            )
        elif isinstance(error, commands.errors.ExpectedClosingQuoteError):
            await ctx.send(
                f"{mention} I only see the starting quote..."
                "are you sure you put an ending quote?"
            )

        # Handle permission errors
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(
                f"{mention} You don't have permission to use that command! "
                "Have someone else do it!"
            )

        # Handle cooldown errors
        elif isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            await ctx.send(
                f"{mention} That command's on cooldown! Wait for "
                f"{h:02}:{m:02}:{s:02}!"
            )

        # Raise the error to the console
        raise error

    @tasks.loop(seconds=5)
    async def change_status(self):
        # Change status from trying the help message to a funny message
        await self.change_presence(activity=discord.Game(next(self.status)))


def main():
    bot = Bot()
    version = __version__
    bot.run(version)

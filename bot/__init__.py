import json
import logging
import os
from itertools import cycle
from secrets import choice

import discord
from discord import Intents
from discord.ext import commands, tasks

# Set up logging
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)


class Bot(commands.Bot):
    def __init__(self):
        # Load settings from settings.json
        self.settings = json.loads(open("./settings.json", "r").read())

        # Token and command prefix
        self.token = self.settings["token"]
        self.prefix = self.settings["prefix"]

        # Respond to self / other bots
        self.respond_to_self = self.settings["respond_to_self"]
        self.respond_to_bots = self.settings["respond_to_bots"]

        # Ready messages and status change messages
        with open("./ready_responses.txt") as file:
            self.ready = [response.strip() for response in file.readlines()]
        self.status = cycle([f"Try {self.prefix}help!", "with 1s and 0s"])

        # Client initialization
        super().__init__(command_prefix=self.prefix, intents=Intents.all())

    def run(self, version):
        self.version = version
        super().run(self.token, reconnect=True)

    # Start status changing loop and print ready message
    async def on_ready(self):
        # Load cogs
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"cogs.{filename[:-3]}")

        self.change_status.start()
        print(choice(self.ready))

    # Error handling
    async def on_command_error(self, ctx, error):
        mention = ctx.author.mention
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(
                f"{mention} That's not a valid command! "
                f"Type `{self.prefix}help` for a list of commands."
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
        else:
            await ctx.send(
                f"{mention} Oops! There was an error I couldn't identify: " f"{error}"
            )

    # Message handling
    async def on_message(self, message):
        # Make sure bot doesn't respond to itself
        if (
            message.author.id == self.user.id
            and self.respond_to_self.lower() == "false"
        ):
            return

        # Make sure bot doesn't respond to other bots
        if message.author.bot and self.respond_to_bots.lower() == "false":
            return

        await self.process_commands(message)

    # Change status from trying the help message to a funny message
    @tasks.loop(seconds=5)
    async def change_status(self):
        await self.change_presence(activity=discord.Game(next(self.status)))


# Bot variable
bot = Bot()

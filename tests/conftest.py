import discord.ext.commands as commands
import discord.ext.test as dpytest

import pytest


@pytest.fixture()
async def bot():
    bot = commands.Bot(command_prefix="$")

    dpytest.configure(bot)

    yield bot

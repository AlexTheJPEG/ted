import discord.ext.test as dpytest

import pytest


@pytest.fixture(autouse=True)
def bot_help(bot):
    bot.load_extension("cogs.help")
    bot.load_extension("cogs.ping")
    dpytest.configure(bot)
    return bot


@pytest.mark.asyncio
async def test_help():
    await dpytest.message("$help")
    dpytest.verify_message(text="To get help on a specific command", contains=True)


@pytest.mark.asyncio
async def test_help_with_invalid_command():
    await dpytest.message("$help asdf")
    dpytest.verify_message(text="That's not a valid command!", contains=True)


@pytest.mark.asyncio
async def test_help_with_command():
    await dpytest.message("$help ping")
    dpytest.verify_message(text="To bring up this message again", contains=True)

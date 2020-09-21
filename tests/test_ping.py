import discord.ext.test as dpytest

import pytest


@pytest.fixture(autouse=True)
def bot_help(bot):
    bot.load_extension("cogs.ping")
    dpytest.configure(bot)
    return bot


@pytest.mark.asyncio
async def test_ping():
    await dpytest.message("$ping")
    dpytest.verify_message(text="Pong!", contains=True)

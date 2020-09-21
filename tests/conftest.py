import discord.ext.commands as commands
import discord.ext.test as dpytest

import pytest


@pytest.fixture()
async def bot():
    bot = commands.Bot(command_prefix="$", help_command=None)

    dpytest.configure(bot)

    test_guild = dpytest.backend.make_guild("Test Guild")
    dpytest.backend.make_text_channel("general", test_guild)
    test_user = dpytest.backend.make_user("TestUser", "8008")
    dpytest.backend.make_member(test_user, test_guild, "TestUser")

    yield bot

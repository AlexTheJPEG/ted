import discord.ext.test as dpytest

import pytest


@pytest.fixture(autouse=True)
def bot_help(bot):
    bot.load_extension("cogs.rand")
    dpytest.configure(bot)
    return bot


@pytest.mark.asyncio
async def test_8ball():
    await dpytest.message("$8ball test")
    dpytest.verify_message(text="🎱", contains=True)


@pytest.mark.asyncio
async def test_roll_default():
    await dpytest.message("$roll")
    dpytest.verify_message(text="rolled a 1d6", contains=True)


@pytest.mark.asyncio
async def test_roll_non_default():
    await dpytest.message("$roll 3d10")
    dpytest.verify_message(text="rolled a 3d10", contains=True)


@pytest.mark.asyncio
async def test_roll_too_big():
    await dpytest.message("$roll 1000d1000")
    dpytest.verify_message(text="Your roll is too big!", contains=True)


@pytest.mark.asyncio
async def test_roll_non_number():
    await dpytest.message("$roll 1dF")
    dpytest.verify_message(text="Make sure both sides", contains=True)


@pytest.mark.asyncio
async def test_roll_invalid_notation():
    await dpytest.message("$roll blah")
    dpytest.verify_message(text="Your roll isn't in dice notation!", contains=True)


@pytest.mark.asyncio
async def test_coin():
    await dpytest.message("$coin")
    dpytest.verify_message(text="It's", contains=True)


@pytest.mark.asyncio
async def test_lottery_powerball():
    await dpytest.message("$lottery powerball")
    dpytest.verify_message(text="Here are your Powerball numbers:", contains=True)


@pytest.mark.asyncio
async def test_lottery_megamillions():
    await dpytest.message("$lottery megamillions")
    dpytest.verify_message(text="Here are your Mega Millions numbers:", contains=True)


@pytest.mark.asyncio
async def test_lottery_euromillions():
    await dpytest.message("$lottery euromillions")
    dpytest.verify_message(text="Here are your EuroMillions numbers:", contains=True)


@pytest.mark.asyncio
async def test_lottery_invalid():
    await dpytest.message("$lottery blah")
    dpytest.verify_message(text="That's not a valid lottery game!", contains=True)

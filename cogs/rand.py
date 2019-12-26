import discord
import random
import os
from discord.ext import commands


class Rand(commands.Cog):
    def __init__(self, client):
        self.client = client

        eb_responses_path = os.getcwd() + "/cogs/8ball/"
        eb_path_positive = eb_responses_path + "positive.txt"
        eb_path_negative = eb_responses_path + "negative.txt"
        eb_path_uncertain = eb_responses_path + "uncertain.txt"
        with open(eb_path_positive) as positive, open(eb_path_negative) as negative, open(eb_path_uncertain) as uncertain:
            self.eb_responses_positive = [response.strip() for response in positive.readlines()]
            self.eb_responses_negative = [response.strip() for response in negative.readlines()]
            self.eb_responses_uncertain = [response.strip() for response in uncertain.readlines()]
        if not (len(self.eb_responses_positive) == len(self.eb_responses_negative) == len(self.eb_responses_uncertain)):
            print("""[WARNING] The positive, negative, and uncertain responses for eightball don't have the same amount of responses.""")
        self.eb_responses = self.eb_responses_positive + self.eb_responses_negative + self.eb_responses_uncertain

    @commands.command(name="8ball")
    async def eightball(self, ctx, question: str):
        mention = ctx.author.mention
        # Pick a random response
        await ctx.send(f"{mention} | :8ball: | {random.choice(self.eb_responses)}")

    @commands.command()
    async def roll(self, ctx, d="1d6"):
        mention = ctx.author.mention
        dice = d.partition('d')
        if dice[1] == "d":
            try:
                # Get the number of dice to roll and the number of sides on each die
                number = int(dice[0])
                sides = int(dice[2])
                # Generate rolls
                rolls = [random.randint(1, sides) for _ in range(number)]
                try:
                    mention = ctx.author.mention
                    await ctx.send(f""":game_die: {mention} rolled a {''.join(d)} and got:
```{', '.join(list(map(str, rolls)))}```
```Max:\t\t{max(rolls)}
Min:\t\t{min(rolls)}
Sum:\t\t{sum(rolls)}
Average:\t{sum(rolls) / len(rolls)}```""")
                except discord.errors.HTTPException:
                    # If the rolls formatted into text goes past the character limit
                    await ctx.send(f"{mention} Your roll is too big! Try having fewer sides or using fewer dice.")
            except ValueError:
                await ctx.send(f"{mention} Make sure both sides of the dice notation are numbers!")
        else:
            await ctx.send(f"{mention} Your roll isn't in dice notation! Type `{ctx.prefix}help roll` for more info.")

    @commands.command()
    async def coin(self, ctx):
        # Heads or tails. That's it.
        mention = ctx.author.mention
        c = random.randint(0, 1)
        if bool(c):
            await ctx.send(f"{mention} It's heads.")
        else:
            await ctx.send(f"{mention} It's tails.")

    @commands.command()
    async def lottery(self, ctx, game):
        mention = ctx.author.mention
        if game == "powerball":
            # (USA) Powerball
            # Five numbers (1-69) + one powerball number (1-26)
            five_numbers = [random.randint(1, 69) for _ in range(5)]
            powerball_number = random.randint(1, 26)
            await ctx.send(f""":moneybag: {mention} Here are your Powerball numbers:
```{', '.join(list(map(str, five_numbers)))} ({powerball_number})```""")
        elif game == "megamillions":
            # (USA) Mega Millions
            # Five numbers (1-70) + one megaball number (1-25)
            five_numbers = [random.randint(1, 70) for _ in range(5)]
            megaball_number = random.randint(1, 25)
            await ctx.send(f""":moneybag: {mention} Here are your Mega Millions numbers:
```{', '.join(list(map(str, five_numbers)))} ({megaball_number})```""")
        elif game == "euromillions":
            # (EUR) EuroMillions
            # Five numbers (1-50) + two lucky star numbers (1-12)
            five_numbers = [random.randint(1, 50) for _ in range(5)]
            lucky_star_numbers = [random.randint(1, 12) for _ in range(2)]
            await ctx.send(f""":moneybag: {mention} Here are your EuroMillions numbers:
```{', '.join(list(map(str, five_numbers)))} ({' '.join(list(map(str, lucky_star_numbers)))})```""")


def setup(client):
    client.add_cog(Rand(client))

import os
from secrets import SystemRandom

from discord.ext import commands


class Rand(commands.Cog):
    def __init__(self, client):
        """Cog for commands that involve randomness.

        Args:
            client (commands.Bot): The bot that the cog belongs to.
        """
        self.client = client

        self.init_eight_ball()

        self.random_gen = SystemRandom()

    def init_eight_ball(self):
        eb_responses_path = os.getcwd() + "/cogs/8ball/"
        eb_path_positive = eb_responses_path + "positive.txt"
        eb_path_negative = eb_responses_path + "negative.txt"
        eb_path_uncertain = eb_responses_path + "uncertain.txt"
        with open(eb_path_positive) as positive, open(
            eb_path_negative
        ) as negative, open(eb_path_uncertain) as uncertain:
            self.eb_responses_positive = [
                response.strip() for response in positive.readlines()
            ]
            self.eb_responses_negative = [
                response.strip() for response in negative.readlines()
            ]
            self.eb_responses_uncertain = [
                response.strip() for response in uncertain.readlines()
            ]
        if not (
            len(self.eb_responses_positive)
            == len(self.eb_responses_negative)
            == len(self.eb_responses_uncertain)
        ):
            print(
                "[WARNING] The positive, negative, and uncertain responses for "
                "eightball don't have the same amount of responses."
            )
        self.eb_responses = (
            self.eb_responses_positive
            + self.eb_responses_negative
            + self.eb_responses_uncertain
        )

    @commands.command(name="8ball")
    async def eightball(self, ctx, question: str):
        mention = ctx.author.mention

        # Pick a random response
        choice = self.random_gen.choice(self.eb_responses)

        # Add the corresponding emoji
        if choice in self.eb_responses_positive:
            choice = "✔ " + choice
        elif choice in self.eb_responses_negative:
            choice = "❌ " + choice
        elif choice in self.eb_responses_uncertain:
            choice = "❔ " + choice

        await ctx.send(f"🎱 {mention} {choice}")

    @commands.command()
    async def roll(self, ctx, d="1d6"):
        mention = ctx.author.mention
        dice = d.partition("d")
        if dice[1] == "d":
            try:
                # Get the number of dice to roll and the number of sides on each die
                number = int(dice[0])
                sides = int(dice[2])
                # Generate rolls
                rolls = [self.random_gen.randint(1, sides) for _ in range(number)]
                roll_string = f"🎲 {mention} rolled a {''.join(d)} and got:" \
                              f"\n```{', '.join(list(map(str, rolls)))}```" \
                              f"\n```Max:\t\t{max(rolls)}" \
                              f"\nMin:\t\t{min(rolls)}" \
                              f"\nSum:\t\t{sum(rolls)}" \
                              f"\nAverage:\t{sum(rolls) / len(rolls)}```"
                if len(roll_string) <= 2000:
                    mention = ctx.author.mention
                    await ctx.send(roll_string)
                else:
                    # If the rolls formatted into text goes past the character limit
                    await ctx.send(
                        f"❗ {mention} Your roll is too big! "
                        "Try having fewer sides or using fewer dice."
                    )
            except ValueError:
                # If the dice notation is invalid
                await ctx.send(
                    f"❗ {mention} Make sure both sides of "
                    "the dice notation are numbers!"
                )
        else:
            # If the roll is not in dice notation
            await ctx.send(
                f"❗ {mention} Your roll isn't in dice notation! "
                f"Type `{ctx.prefix}help roll` for more info."
            )

    @commands.command()
    async def coin(self, ctx):
        # Heads or tails. That's it.
        mention = ctx.author.mention
        coin = self.random_gen.randint(0, 1)
        if bool(coin):
            await ctx.send(f"{mention} It's heads.")
        else:
            await ctx.send(f"{mention} It's tails.")

    @commands.command()
    async def lottery(self, ctx, game):
        mention = ctx.author.mention
        if game == "powerball":
            # (USA) Powerball
            # Five numbers (1-69) + one powerball number (1-26)
            five_numbers = [self.random_gen.randint(1, 69) for _ in range(5)]
            five_numbers_formatted = ", ".join(list(map(str, five_numbers)))
            powerball_number = self.random_gen.randint(1, 26)
            await ctx.send(
                f"💰 {mention} Here are your Powerball numbers:"
                f"\n```{five_numbers_formatted} ({powerball_number})```"
            )
        elif game == "megamillions":
            # (USA) Mega Millions
            # Five numbers (1-70) + one megaball number (1-25)
            five_numbers = [self.random_gen.randint(1, 70) for _ in range(5)]
            five_numbers_formatted = ", ".join(list(map(str, five_numbers)))
            megaball_number = self.random_gen.randint(1, 25)
            await ctx.send(
                f"💰 {mention} Here are your Mega Millions numbers:"
                f"\n```{five_numbers_formatted} ({megaball_number})```"
            )
        elif game == "euromillions":
            # (EUR) EuroMillions
            # Five numbers (1-50) + two lucky star numbers (1-12)
            five_numbers = [self.random_gen.randint(1, 50) for _ in range(5)]
            five_numbers_formatted = ", ".join(list(map(str, five_numbers)))
            lucky_star_numbers = [self.random_gen.randint(1, 12) for _ in range(2)]
            lucky_star_numbers_formatted = " ".join(list(map(str, lucky_star_numbers)))
            await ctx.send(
                f"💰 {mention} Here are your EuroMillions numbers:"
                f"\n```{five_numbers_formatted} ({lucky_star_numbers_formatted})```"
            )
        else:
            await ctx.send(f"❗ {mention} That's not a valid lottery game! "
                           "You can choos from `powerball`, `megamillions`, "
                           "and `euromillions`.")


def setup(client):
    client.add_cog(Rand(client))

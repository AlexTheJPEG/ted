import discord
import random
from discord.ext import commands


class Rand(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.eb_responses_positive = ["Yes", "As I see it, yes", "It is certain", "It is decidedly so",
                                      "Without a doubt", "Definitely", "You may rely on it", "Most likely",
                                      "Outlook good", "Signs point to yes", "Probably", "Affirmative", "Absolutely",
                                      "Unfortunately, yes", "Fortunately, yes", "I'm going for yes", ":100: :ok_hand:",
                                      "Yep", "Yes, yes, yes!!"]
        self.eb_responses_negative = ["No", "Probably not", "Don't count on it", "My reply is no", "My sources say no",
                                      "Outlook not so good", "Very doubtful", "I don't think so", "Signs point to no",
                                      "Negative", "Absolutely not", "Unfortunately, no", "Fortunately, no",
                                      "Not happening", "Leaning towards no", "Definitely not", "Not a chance",
                                      "That's a no from me chief", "ERROR 403: Forbidden"]
        self.eb_responses_uncertain = ["Maybe", "Reply hazy, try again", "Ask again later", "Better not tell you now",
                                       "Cannot predict now", "Concentrate and ask again", "I don't know", "Who knows?",
                                       "Uncertain at the moment", "Whatever you think the answer should be", "Perhaps",
                                       "Can't tell you just yet", "I'm not sure", "It depends on the circumstances",
                                       "Try asking another time", "It's up to you to decide that", "Too lazy to answer",
                                       "ERROR 404: Answer not found", "Huh?"]
        if not (len(self.eb_responses_positive) == len(self.eb_responses_negative) == len(self.eb_responses_uncertain)):
            print("""[WARNING] The positive, negative, and uncertain responses for eightball don't have the same amount of responses.""")
        self.eb_responses = self.eb_responses_positive + self.eb_responses_negative + self.eb_responses_uncertain

    @commands.command(name="8ball")
    async def eightball(self, ctx, question: str):
        mention = ctx.message.author.mention
        # Pick a random response
        await ctx.send(f"{mention} | :8ball: | {random.choice(self.eb_responses)}")

    @commands.command(aliases=["dice"])
    async def roll(self, ctx, d: str):
        mention = ctx.message.author.mention
        dice = d.partition('d')
        if dice[1] == "d":
            try:
                # Get the number of dice to roll and the number of sides on each die
                number = int(dice[0])
                sides = int(dice[2])
                # Generate rolls
                rolls = [random.randint(1, sides) for _ in range(number)]
                try:
                    mention = ctx.message.author.mention
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
        mention = ctx.message.author.mention
        c = random.randint(0, 1)
        if bool(c):
            await ctx.send(f"{mention} It's heads.")
        else:
            await ctx.send(f"{mention} It's tails.")

    @commands.command()
    async def lottery(self, ctx, game):
        mention = ctx.message.author.mention
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

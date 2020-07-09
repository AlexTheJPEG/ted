import asyncio
import random

from discord.ext import commands


class Games(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.rps_moves = {
            "rock": ["scissors", "paper"],
            "paper": ["rock", "scissors"],
            "scissors": ["paper", "rock"],
        }
        self.rps_emotes = {"rock": "✊", "paper": "✋", "scissors": "✌"}

    @commands.command()
    async def rps(self, ctx, move=""):
        mention = ctx.author.mention
        if move.lower() not in self.rps_moves.keys():
            await ctx.send(f"{mention} That's not a valid move!")
        else:
            bot_move = random.choice(list(self.rps_moves.keys()))

            await ctx.send(f"✊✋✌ {mention} Rock, paper, scissors, shoot!")
            await asyncio.sleep(2)

            await ctx.send(
                "You     Me"
                f"\n{self.rps_emotes[move]}      {self.rps_emotes[bot_move]}"
            )

            if move == self.rps_moves[bot_move][0]:
                await ctx.send(f"{mention} I win!")
            elif move == self.rps_moves[bot_move][1]:
                await ctx.send(f"{mention} You win.")
            else:
                await ctx.send(f"{mention} It's a draw.")

    @commands.command()
    async def guessinggame(self, ctx, highest=100):
        mention = ctx.author.mention
        play = True

        # Check number for validity
        if highest in range(2, 1_000_001):
            if highest >= 100_000:
                await ctx.send(
                    f"❓ {mention} A game with this max will take a while! "
                    "Are you sure you want to do this? "
                    "Type `yes` to confirm or anything else to cancel."
                )
                yn = await self.client.wait_for("message")
                if yn.content.lower() != "yes":
                    await ctx.send(f"{mention} Your game was cancelled.")
                    play = False
        else:
            raise commands.errors.BadArgument

        if play:
            # Starting prompt
            await ctx.send(
                f"💭 {mention} I'm thinking of a number between 1 and {highest}. "
                "You can cancel this game at any time by typing `cancel`."
            )
            number = random.randint(1, highest)
            guesses = 0

        # Game loop
        while play:
            guess = await self.client.wait_for("message")
            if guess.content == "cancel":
                # Player cancelled the game
                await ctx.send(f"{mention} Your game was cancelled.")
                play = False
            elif guess.content.isdigit():
                # Player entered a number
                guess = int(guess.content)
                if guess not in range(1, highest + 1):
                    # The number is outside of the specified range
                    await ctx.send(
                        f"❗ {mention} That's not a number between 1 and {highest}!"
                    )
                else:
                    # The number is valid
                    guesses += 1
                    if guess > number:
                        # The guess is lower than the answer
                        await ctx.send(f"🔽 {mention} My number is lower.")
                    elif guess < number:
                        # The guess is higher than the number
                        await ctx.send(f"🔼 {mention} My number is higher.")
                    else:
                        # The player got the number right
                        if guesses > 1:
                            await ctx.send(
                                f"👍 {mention} You got it! It took you {guesses} tries."
                            )
                        else:
                            # The player got it on their first try
                            await ctx.send(
                                f"🤯 {mention} Unbelievable! "
                                "You got it on your first try!!"
                            )
                        play = False

    @guessinggame.error
    async def guessinggame_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(
                "❗ That's not a valid number! If you want to specify a number, "
                "make sure that it's actually a number "
                "and that it's in between 2 and 1,000,000."
            )


def setup(client):
    client.add_cog(Games(client))

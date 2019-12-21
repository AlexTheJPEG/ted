import asyncio
import random
from discord.ext import commands


class Games(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.rps_moves = {"rock": ["scissors", "paper"],
                          "paper": ["rock", "scissors"],
                          "scissors": ["paper", "rock"]}
        self.rps_emotes = {"rock": "👊",
                           "paper": "✋",
                           "scissors": "✌"}

    @commands.command()
    async def rps(self, ctx, move=""):
        mention = ctx.message.author.mention
        if move.lower() not in self.rps_moves.keys():
            await ctx.send(f"{mention} That's not a valid move!")
        else:
            bot_move = random.choice(list(self.rps_moves.keys()))

            await ctx.send(f"{mention} Rock, paper, scissors, shoot!")
            await asyncio.sleep(2)

            await ctx.send(f"""You     Me
{self.rps_emotes[move]}      {self.rps_emotes[bot_move]}""")

            if move == self.rps_moves[bot_move][0]:
                await ctx.send(f"{mention} I win!")
            elif move == self.rps_moves[bot_move][1]:
                await ctx.send(f"{mention} You win.")
            else:
                await ctx.send(f"{mention} It's a draw.")


def setup(client):
    client.add_cog(Games(client))

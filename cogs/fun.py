import os
import random

from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        slap_texts_path = os.getcwd() + "/cogs/slap/slaps.txt"
        with open(slap_texts_path, errors="ignore") as slaps:
            self.slap_texts = [slap.strip() for slap in slaps.readlines()]

    def create_ground_string(self, groundee, reason):
        time = random.randint(10 ** 50, 99 ** 50)
        oh = "OH" * random.randint(15, 30)
        grounded = ("GROUNDED " * random.randint(7, 15)).strip()
        time_unit = random.choice(["YEARS", "CENTURIES", "EONS", "ETERNITIES"])
        return (
            f"{oh} {groundee.upper()} HOW DARE YOU {reason.upper()}!!! "
            f"THAT'S IT. YOU ARE {grounded} FOR {time} {time_unit}!!!!!!!!!!"
        )

    @commands.command()
    async def thegame(self, ctx):
        await ctx.send("I lost The Game.", tts=True)

    @commands.command()
    async def whendidijoin(self, ctx):
        mention = ctx.author.mention
        if ctx.guild is None:
            await ctx.send(
                "It seems you are not using this command on a server. "
                "Go to a server and use this command again!"
            )
        else:
            await ctx.send(
                f"🕒 {mention} Your very first time joining **{ctx.guild.name}** "
                f"was on {ctx.author.joined_at}!"
            )

    @commands.command()
    async def ground(self, ctx, groundee, reason):
        await ctx.send(self.create_ground_string(groundee, reason))

    @commands.command()
    async def slap(self, ctx, slappee):
        await ctx.send(random.choice(self.slap_texts).format(slappee))

    @ground.error
    async def ground_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            mention = ctx.author.mention
            await ctx.send(
                self.create_ground_string(
                    mention, "not pass in the correct amount of arguments"
                )
            )


def setup(client):
    client.add_cog(Fun(client))

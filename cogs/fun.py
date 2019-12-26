from discord.ext import commands
import random


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    def create_ground_string(self, groundee, reason):
        time = random.randint(10 ** 50, 99 ** 50)
        oh = "OH" * random.randint(15, 30)
        grounded = ("GROUNDED " * random.randint(7, 15)).strip()
        time_unit = random.choice(['YEARS', 'CENTURIES', 'EONS', 'ETERNITIES'])
        return f"{oh} {groundee.upper()} HOW DARE YOU {reason.upper()}!!! THAT'S IT. YOU ARE {grounded} FOR {time} {time_unit}!!!!!!!!!!"

    @commands.command()
    async def thegame(self, ctx):
        await ctx.send("I lost The Game.", tts=True)

    @commands.command()
    async def whendidijoin(self, ctx):
        mention = ctx.message.author.mention
        if ctx.guild is None:
            await ctx.send("It seems you are not using this command on a server. Go to a server and use this command again!")
        else:
            await ctx.send(f"{mention} Your very first time joining **{ctx.guild.name}** was on {ctx.author.joined_at}!")

    @commands.command()
    async def ground(self, ctx, groundee, reason):

        await ctx.send(self.create_ground_string(groundee, reason))

    @ground.error
    async def ground_error(self, ctx, error):
        mention = ctx.message.author.mention
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(self.create_ground_string(mention, "not pass in the correct amount of arguments"))


def setup(client):
    client.add_cog(Fun(client))

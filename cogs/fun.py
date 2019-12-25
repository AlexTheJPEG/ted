from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def thegame(self, ctx):
        await ctx.send("I lost The Game.", tts=True)


def setup(client):
    client.add_cog(Fun(client))

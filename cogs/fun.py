from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

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


def setup(client):
    client.add_cog(Fun(client))

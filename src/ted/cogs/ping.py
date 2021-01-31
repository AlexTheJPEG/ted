from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, client):
        """Cog for pinging the bot.

        Args:
            client (commands.Bot): The bot that the cog belongs to.
        """
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        # ? Is this accurate?
        mention = ctx.author.mention
        await ctx.send(
            f"🏓 {mention} Pong! " f"(**{round(self.client.latency * 1000, 1)}ms**)"
        )


def setup(client):
    client.add_cog(Ping(client))

from discord.ext import commands


class Image(commands.Cog):
    def __init__(self, client):
        """Cog for image manipulation.

        Args:
            client (commands.Bot): The bot that the cog belongs to.
        """
        self.client = client

    @commands.command()
    async def avatar(self, ctx, user):
        user = ctx.guild.get_member_named(user)
        avatar_url = user.avatar_url_as(format="png")

        # TODO: send actual image
        await ctx.send(avatar_url)


def setup(client):
    client.add_cog(Image(client))

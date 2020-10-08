from discord.ext import commands


class Image(commands.Cog):
    def __init__(self, client):
        """Cog for image manipulation.

        Args:
            client (commands.Bot): The bot that the cog belongs to.
        """
        self.client = client

    @commands.command()
    async def avatar(self, ctx, user=""):
        member = ctx.author if not user else ctx.guild.get_member_named(user)
        print(member is None)
        avatar_url = member.avatar_url_as(format="png")

        await ctx.send(avatar_url)


def setup(client):
    client.add_cog(Image(client))

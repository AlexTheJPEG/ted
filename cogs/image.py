from discord.ext import commands


class Image(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def avatar(self, ctx, user):
        user = ctx.guild.get_member_named(user)
        avatar_url = user.avatar_url_as(format="png")

        # TODO: send actual image
        await ctx.send(avatar_url)


def setup(client):
    client.add_cog(Image(client))

import os

from PIL import Image, ImageChops

import discord
from discord.ext import commands

import requests


class Images(commands.Cog):
    def __init__(self, client):
        """Cog for image manipulation.

        Args:
            client (commands.Bot): The bot that the cog belongs to.
        """
        self.client = client

    @commands.command()
    async def avatar(self, ctx, user=""):
        if user.startswith("<@!"):
            member = ctx.guild.get_member(int(user[3:-1]))
        else:
            member = ctx.author if not user else ctx.guild.get_member_named(user)

        avatar_url = requests.get(member.avatar_url_as(format="png"))
        filename = f"{ctx.author.id}.png"

        with open(filename, "wb") as img:
            img.write(avatar_url.content)

        await ctx.send(file=discord.File(filename))

        os.remove(filename)


def setup(client):
    client.add_cog(Images(client))

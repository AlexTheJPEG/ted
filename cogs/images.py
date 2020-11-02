import os

from PIL import Image, ImageChops, ImageEnhance, ImageOps

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

        avatar = requests.get(member.avatar_url_as(format="png"))
        filename = f"{ctx.author.id}.png"

        with open(filename, "wb") as img:
            img.write(avatar.content)

        await ctx.send(file=discord.File(filename))

        os.remove(filename)

    @commands.command()
    async def invert(self, ctx):
        image_url = ctx.message.attachments[0].url
        image_bytes = requests.get(image_url)
        filename = f"{ctx.author.id}.png"

        with open(filename, "wb") as img:
            img.write(image_bytes.content)

        img = Image.open(filename)
        img = Image.composite(img, Image.new("RGB", img.size, "white"), img)

        inverted_img = ImageChops.invert(img)
        inverted_img.save(filename)

        img.close()
        inverted_img.close()

        await ctx.send(file=discord.File(filename))

        os.remove(filename)


def setup(client):
    client.add_cog(Images(client))

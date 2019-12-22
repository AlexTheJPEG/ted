from discord.ext import commands
from googletrans import Translator
from googletrans.constants import LANGUAGES


class Translate(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.langcodes = list(LANGUAGES.keys())

    @commands.command()
    async def translate(self, ctx, src, des, phrase):
        mention = ctx.message.author.mention
        pass

    @commands.command()
    async def badtranslate(self, ctx, src, des, phrase):
        mention = ctx.message.author.mention
        pass

    @commands.command()
    async def langcodes(self, ctx, src, des, phrase):
        mention = ctx.message.author.mention
        pass


def setup(client):
    client.add_cog(Translate(client))

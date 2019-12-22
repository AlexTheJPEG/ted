from discord.ext import commands
from googletrans import Translator
from googletrans.constants import LANGUAGES


class Translate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def translate(self, ctx, src, des, phrase):
        mention = ctx.message.author.mention
        pass

    @commands.command()
    async def badtranslate(self, ctx, src, des, phrase):
        mention = ctx.message.author.mention
        pass

    @commands.command()
    async def langcodes(self, ctx):
        author = ctx.message.author
        codes = [f"{key.rjust(5)} - {value.title()}" for (key, value) in LANGUAGES.items()]
        formatted_codes = '\n'.join(codes)

        # Send message
        await author.send(f"""Here are a list of codes you can use for `{ctx.prefix}translate` and `{ctx.prefix}badtranslate`:
```
{formatted_codes}
```""")


def setup(client):
    client.add_cog(Translate(client))

from discord.ext import commands
from googletrans import Translator
from googletrans.constants import LANGUAGES


class Translate(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.translator = Translator()
        self.codes = list(LANGUAGES.keys())

    @commands.command()
    async def translate(self, ctx, src, des, phrase):
        mention = ctx.message.author.mention
        if src == "detect" and des in self.codes:
            # Automatically detect the language
            await ctx.send(f"""{mention} Translation to {des}:
{self.translator.translate(phrase, dest=des).text}""")
        elif src in self.codes and des in self.codes:
            # Use the specified language
            await ctx.send(f"""{mention} Translation from {src} to {des}:
{self.translator.translate(phrase, src=src, dest=des).text}""")
        else:
            # Something went wrong
            await ctx.send(f"""{mention} Make sure that both the source and destination arguments are actual language codes!
Also remember to use the syntax: `{ctx.prefix}translate (source) (destination) (phrase)`
If you want me to automatically detect your language, remember to make `(source)` `detect`.
If the phrase is multiple words, surround it in " quotes \"""")


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

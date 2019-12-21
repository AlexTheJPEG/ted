import discord
from discord.ext import commands


class React(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.number_emotes = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    @commands.command()
    async def yesno(self, ctx, question=""):
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        try:
            poll = await ctx.send(question)
            await poll.add_reaction("👍")
            await poll.add_reaction("👎")
        except discord.HTTPException:
            # If question is empty
            await ctx.send("What is your question?")
        except discord.ext.commands.errors.InvalidEndOfQuotedStringError:
            # If there's something after the quotation
            # like "hello"hi
            await ctx.send("Make sure your entire question is in quotes and there's nothing after the quotes!")
        except discord.ext.commands.errors.ExpectedClosingQuoteError:
            # If there's only one quotation
            # like "hello
            await ctx.send("I only see the starting quote...are you sure you put an ending quote?")

    @commands.command(aliases=["scale"])
    async def numbers(self, ctx, question=""):
        try:
            poll = await ctx.send(question)
            for emote in self.number_emotes:
                await poll.add_reaction(emote)
        # ! This doesn't work for some reason
        except commands.errors.InvalidEndOfQuotedStringError:
            # If there's something after the quotation
            # like "hello"hi
            await ctx.send("Make sure your entire question is in quotes and there's nothing after the quotes!")
        except commands.errors.ExpectedClosingQuoteError:
            # If there's only one quotation
            # like "hello
            await ctx.send("I only see the starting quote...are you sure you put an ending quote?")
        except discord.HTTPException:
            # If question is empty
            await ctx.send("What is your question?")


def setup(client):
    client.add_cog(React(client))

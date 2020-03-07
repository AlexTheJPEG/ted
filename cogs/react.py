from discord.ext import commands


class React(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.yesno_emotes = ["👍", "👎"]
        self.number_emotes = [
            "1️⃣",
            "2️⃣",
            "3️⃣",
            "4️⃣",
            "5️⃣",
            "6️⃣",
            "7️⃣",
            "8️⃣",
            "9️⃣",
            "🔟",
        ]

    @commands.command()
    async def yesno(self, ctx, question=""):
        if question != "":
            poll = await ctx.send(question)
            for emote in self.yesno_emotes:
                await poll.add_reaction(emote)
        else:
            await ctx.send("What is your question?")

    @commands.command(aliases=["scale"])
    async def numbers(self, ctx, question=""):
        if question != "":
            poll = await ctx.send(question)
            for emote in self.number_emotes:
                await poll.add_reaction(emote)
        else:
            await ctx.send("What is your question?")


def setup(client):
    client.add_cog(React(client))

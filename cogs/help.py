import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, command=""):
        command_names = [command.name for command in self.client.commands]
        if command not in command_names:
            author = ctx.message.author
            embed = discord.Embed(colour=13399553)

            embed.set_image(url="https://cdn.discordapp.com/avatars/457280200078524421/a66cc42e800589c1296fcc2665270e62.png")

            embed.set_author(name="Ted's List of Commands", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")

            embed.add_field(name="PING", value="`ping`")
            embed.add_field(name="RANDOM", value="`8ball` `roll` `coin` `lottery`")
            embed.add_field(name="REACTIONS", value="`yesno` `numbers`")

            await author.send(content=f"""To get help on a specific command, type `{ctx.prefix}help (command)`
To bring up this message again, type `{ctx.prefix}help`!""", embed=embed)
        else:
            print(command)


def setup(client):
    client.remove_command("help")
    client.add_cog(Help(client))

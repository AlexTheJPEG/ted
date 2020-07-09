import json
import os

import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.help_texts_path = os.getcwd() + "/cogs/"
        self.help_texts = json.loads(
            open(self.help_texts_path + "help.json", "r").read()
        )

    @commands.command()
    async def help(self, ctx, command=""):
        command_names = [command.name for command in self.client.commands]
        author = ctx.message.author
        embed = discord.Embed(colour=13399553)
        embed.set_image(
            url="https://cdn.discordapp.com/avatars/457280200078524421/"
            "a66cc42e800589c1296fcc2665270e62.png"
        )

        if command != "" and command not in command_names:
            await ctx.send(
                "❗ That's not a valid command! "
                f"Type `{ctx.prefix}help` for a list of commands to get help on."
            )
        elif command == "" or command in "help":
            embed.set_author(
                name="Ted's List of Commands",
                url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            )

            embed.add_field(name="PING", value="`ping`")
            embed.add_field(name="RANDOM", value="`8ball` `roll` `coin` `lottery`")
            embed.add_field(name="REACTIONS", value="`yesno` `numbers`")
            embed.add_field(name="GAMES", value="`rps` `guessinggame`")
            embed.add_field(
                name="TRANSLATE", value="`langcodes` `translate` `badtranslate`"
            )
            embed.add_field(
                name="FUN", value="`thegame` `whendidijoin` `ground` `slap`"
            )

            await author.send(
                content="To get help on a specific command, "
                f"type `{ctx.prefix}help (command)`. "
                f"To bring up this message again, type `{ctx.prefix}help`!",
                embed=embed,
            )
        else:
            embed.set_author(
                name=f"Ted's List of Commands >>> {command}",
                url=self.help_texts[command]["url"],
            )

            embed.add_field(
                name="USAGE", value=f"{ctx.prefix}{self.help_texts[command]['usage']}"
            )
            embed.add_field(
                name="ARGUMENTS", value=self.help_texts[command]["arguments"]
            )
            embed.add_field(
                name="WHAT IT DOES", value=self.help_texts[command]["what-it-does"]
            )

            await author.send(
                content="To bring up this message again, "
                f"type `{ctx.prefix}help {command}`!",
                embed=embed,
            )


def setup(client):
    client.remove_command("help")
    client.add_cog(Help(client))

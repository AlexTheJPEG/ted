import asyncio
import os
import time

from bot import read_json, write_json

import discord
from discord.ext import commands


class Config(commands.Cog):
    def __init__(self, client):
        """Configuration cog for setup and development purposes.

        Args:
            client (commands.Bot): The bot that the cog belongs to.
        """
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog_to_load=""):
        cogs = [cog for cog in os.listdir("./cogs") if cog.endswith(".py")]
        number_of_cogs = len(cogs)

        loaded_cogs = [k.lower() for k in self.client.cogs.keys()]

        if cog_to_load in loaded_cogs:
            self.client.unload_extension(f"cogs.{cog_to_load}")
            self.client.load_extension(f"cogs.{cog_to_load}")

            await ctx.send(f"👍 Reloaded {cog_to_load}.py!")
        else:
            cogs_reloaded = 0
            for cog in cogs:
                try:
                    time_start = time.time()
                    if cog[:-3] in loaded_cogs:
                        self.client.unload_extension(f"cogs.{cog[:-3]}")
                    self.client.load_extension(f"cogs.{cog[:-3]}")
                    time_end = time.time()

                    duration = round((time_end - time_start) * 1000, 1)
                    await ctx.send(f"👍 Successfully reloaded {cog}! ({duration} ms)")
                    cogs_reloaded += 1
                except Exception as e:
                    await ctx.send(f"👎 Couldn't reload {cog}... {e}")

                await asyncio.sleep(1)

            await ctx.send(f"\nReloaded {cogs_reloaded}/{number_of_cogs} cog(s)!")

    @commands.command()
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send("🚶🏾‍♂️ Aight, imma head out")
        await self.client.logout()

    @commands.command()
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.Member):
        self.client.blacklisted.append(user.id)
        data = read_json("./settings.json")
        data["blacklisted"].append(user.id)
        write_json(data, "./settings.json")
        await ctx.send(f"👍 **{user.name}** has been blacklisted.")

    @commands.command()
    @commands.is_owner()
    async def unblacklist(self, ctx, user: discord.Member):
        self.client.blacklisted.remove(user.id)
        data = read_json("./settings.json")
        data["blacklisted"].remove(user.id)
        write_json(data, "./settings.json")
        await ctx.send(f"👍 **{user.name}** is no longer blacklisted.")


def setup(client):
    client.add_cog(Config(client))

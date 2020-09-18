import asyncio
import os
import time

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
    async def reload(self, ctx):
        cogs = [cog for cog in os.listdir("./cogs") if cog.endswith(".py")]
        cogs_reloaded = 0
        number_of_cogs = len(cogs)

        loaded_cogs = [k.lower() for k in self.client.cogs.keys()]

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


def setup(client):
    client.add_cog(Config(client))

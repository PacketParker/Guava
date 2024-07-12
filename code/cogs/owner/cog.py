from discord.ext import commands


class CogCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.dm_only()
    @commands.is_owner()
    async def cog(self, ctx):
        await ctx.author.send(f"This is a group command. Use `{self.bot.command_prefix}cog load/unload/reload` followed by the name of the cog.")

    @cog.command()
    @commands.dm_only()
    @commands.is_owner()
    async def load(self, ctx: commands.Context, *, cog: str = None):
        if not cog:
            return await ctx.send("No cog provided.")

        cog = cog.lower()
        await self.bot.load_extension(f"cogs.{cog}")

        await ctx.send(f"Cog `{cog}` has been loaded.")

    @load.error
    async def cog_load_error(self, ctx, error):
        if isinstance(error.original, commands.ExtensionAlreadyLoaded):
            return await ctx.send(f"Cog is already loaded.")
        if isinstance(error.original, commands.ExtensionNotFound):
            return await ctx.send("Cog does not exist.")
        else:
            return await ctx.send("An unknown error occurred.")

    @cog.command()
    @commands.dm_only()
    @commands.is_owner()
    async def unload(self, ctx: commands.Context, *, cog: str = None):
        if not cog:
            return await ctx.send("No cog provided.")

        cog = cog.lower()
        await self.bot.unload_extension(f"cogs.{cog}")

        await ctx.send(f"Cog `{cog}` has been unloaded.")

    @unload.error
    async def cog_unload_error(self, ctx, error):
        if isinstance(error.original, commands.ExtensionNotLoaded):
            return await ctx.send("Cog not loaded. It might be that the cog does not exist.")
        else:
            return await ctx.send("An unknown error occurred.")

    @cog.command()
    @commands.dm_only()
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, *, cog: str = None):
        if not cog:
            return await ctx.send("No cog provided.")

        cog = cog.lower()
        await self.bot.reload_extension(f"cogs.{cog}")

        await ctx.send(f"Cog `{cog}` has been reloaded.")

    @reload.error
    async def cog_reload_error(self, ctx, error):
        if isinstance(error.original, commands.ExtensionNotLoaded):
            return await ctx.send("Cog not loaded. It might be that the cog does not exist.")
        else:
            return await ctx.send("An unknown error occurred.")


async def setup(bot):
    await bot.add_cog(CogCommands(bot))

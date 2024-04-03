from discord.ext import commands


class LoadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.dm_only()
    @commands.is_owner()
    async def loadcog(self, ctx: commands.Context, cog: str = None):
        if not cog:
            return await ctx.send("No cog provided.")

        cog = cog.lower()
        await self.bot.load_extension(f"cogs.{cog}")

        await ctx.send(f"Cog {cog} has been loaded")


async def setup(bot):
    await bot.add_cog(LoadCog(bot))

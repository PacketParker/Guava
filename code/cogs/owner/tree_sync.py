from discord.ext import commands
from discord import Object


class TreeSync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.dm_only()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, *, guild: Object = None) -> None:
        if not guild or guild == None:
            await self.bot.tree.sync()
            await ctx.author.send("Synced commands globally")
            return

        elif guild != None:
            self.bot.tree.copy_global_to(guild=guild)
            await self.bot.tree.sync(guild=guild)

        await ctx.author.send(f"Synced the tree to 1 test guild.")

    @sync.error
    async def error_sync(self, ctx, error):
        if isinstance(error, commands.errors.PrivateMessageOnly):
            pass
        else:
            await ctx.author.send("That is not a valid guild ID")


async def setup(bot):
    await bot.add_cog(TreeSync(bot))

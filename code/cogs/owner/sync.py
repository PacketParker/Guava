import discord
from discord.ext import commands


class TreeSync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.dm_only()
    @commands.is_owner()
    async def tree(self, ctx):
        await ctx.author.send(
            "This is a group command. Use either"
            f" `{self.bot.command_prefix}tree sync` or"
            f" `{self.bot.command_prefix}tree clear` followed by an optional"
            " guild ID."
        )

    @commands.dm_only()
    @commands.is_owner()
    @tree.command()
    async def sync(
        self, ctx: commands.Context, *, guild: discord.Object = None
    ):
        """Sync the command tree to a guild or globally."""
        if guild:
            self.bot.tree.copy_global_to(guild=guild)
            await self.bot.tree.sync(guild=guild)
            return await ctx.author.send(
                "Synced the command tree to"
                f" `{self.bot.get_guild(guild.id).name}`"
            )
        else:
            await self.bot.tree.sync()
            return await ctx.author.send("Synced the command tree globally.")

    @sync.error
    async def tree_sync_error(self, ctx, error):
        if isinstance(error, commands.ObjectNotFound):
            return await ctx.author.send(
                "The guild you provided does not exist."
            )
        if isinstance(error, commands.CommandInvokeError):
            return await ctx.author.send(
                "Guild ID provided is not a guild that the bot is in."
            )
        else:
            return await ctx.author.send(
                "An unknown error occurred. Perhaps you've been rate limited."
            )

    @commands.dm_only()
    @commands.is_owner()
    @tree.command()
    async def clear(self, ctx: commands.Context, *, guild: discord.Object):
        """Clear the command tree from a guild."""
        self.bot.tree.clear_commands(guild=guild)
        await self.bot.tree.sync(guild=guild)
        return await ctx.author.send(
            "Cleared the command tree from"
            f" `{self.bot.get_guild(guild.id).name}`"
        )

    @clear.error
    async def tree_sync_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.author.send(
                "You need to provide a guild ID to clear the command tree"
                " from."
            )
        if isinstance(error, commands.ObjectNotFound):
            return await ctx.author.send(
                "The guild you provided does not exist."
            )
        if isinstance(error, commands.CommandInvokeError):
            return await ctx.author.send(
                "Guild ID provided is not a guild that the bot is in."
            )
        else:
            return await ctx.author.send(
                "An unknown error occurred. Perhaps you've been rate limited."
            )


async def setup(bot):
    await bot.add_cog(TreeSync(bot))

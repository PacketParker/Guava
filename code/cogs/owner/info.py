from discord.ext import commands
import discord

from global_variables import BOT_COLOR


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.dm_only()
    @commands.is_owner()
    async def info(self, ctx: commands.Context):
        total_guilds = {}

        for guild in self.bot.guilds:
            total_guilds[guild.name] = guild.member_count

        # Sort the dictionary by value descending
        total_guilds = dict(
            sorted(total_guilds.items(), key=lambda item: item[1], reverse=True)
        )

        total_members = 0

        for guild in total_guilds:
            total_members += total_guilds[guild]

        embed = discord.Embed(
            title="User Count",
            description=f"Total Members: `{total_members:,}`\nTotal Guilds: `{len(self.bot.guilds):,}`\n\nTotal Players: `{self.bot.lavalink.nodes[0].stats.playing_players}`\nLoad: `{round(self.bot.lavalink.nodes[0].stats.lavalink_load * 100, 2)}%`",
            color=BOT_COLOR,
        )
        # Add the top 5 guilds to the embed
        for guild in list(total_guilds)[:5]:
            embed.add_field(
                name=guild, value=f"```{total_guilds[guild]:,}```", inline=False
            )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Info(bot))

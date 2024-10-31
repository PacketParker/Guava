import discord
import datetime
from discord import app_commands
from discord.ext import commands
from cogs.music import Music

from utils.config import BOT_COLOR


class Remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.check(Music.create_player)
    @app_commands.describe(number="Song number to have removed")
    async def remove(self, interaction: discord.Interaction, number: int):
        "Removes the specified song from the queue"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        if not player.queue:
            embed = discord.Embed(
                title="Nothing Queued",
                description=(
                    "Nothing is currently in the queue, so there is nothing"
                    " for me to remove."
                ),
                color=BOT_COLOR,
            )
            embed.set_footer(
                text=datetime.datetime.now(datetime.timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                + " UTC"
            )
            return await interaction.response.send_message(embed=embed)

        if number > len(player.queue) or number < 1:
            return await interaction.response.send_message(
                "The number entered is not a number within the queue - please"
                " try again!",
                ephemeral=True,
            )

        index = number - 1
        removed_title = player.queue[index].title
        removed_url = player.queue[index].uri
        removed_artwork = player.queue[index].artwork_url
        player.queue.pop(index)

        embed = discord.Embed(
            title="Song Removed from Queue",
            description=(
                "**Song Removed -"
                f" [{removed_title}]({removed_url})**\n\nIssued by:"
                f" {interaction.user.mention}"
            ),
            color=BOT_COLOR,
        )
        embed.set_thumbnail(url=removed_artwork)
        embed.set_footer(
            text=datetime.datetime.now(datetime.timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            + " UTC"
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Remove(bot))

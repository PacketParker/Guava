import discord
import datetime
from discord import app_commands
from discord.ext import commands
from cogs.music import Music

from utils.config import create_embed


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
            embed = create_embed(
                title="Nothing Queued",
                description="There are no songs in the queue to remove.",
            )
            return await interaction.response.send_message(
                embed=embed, ephemeral=True
            )

        if number > len(player.queue) or number < 1:
            embed = create_embed(
                title="Number Out of Range",
                description=(
                    "The number you entered is outside of the allowed range."
                    " Please try again with a valid song number."
                ),
            )
            return await interaction.response.send_message(
                embed=embed, ephemeral=True
            )

        index = number - 1
        removed_title = player.queue[index].title
        removed_url = player.queue[index].uri
        removed_artwork = player.queue[index].artwork_url
        player.queue.pop(index)

        embed = create_embed(
            title="Song Removed from Queue",
            description=(
                f"**[{removed_title}]({removed_url})** has been unqueued.\n\n"
                f"Issued by: {interaction.user.mention}"
            ),
            thumbnail=removed_artwork,
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Remove(bot))

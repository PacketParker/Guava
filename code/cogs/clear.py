import discord
import datetime
from discord import app_commands
from discord.ext import commands
from cogs.music import Music

from utils.config import create_embed


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.check(Music.create_player)
    async def clear(self, interaction: discord.Interaction):
        "Clear the entire queue of songs"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        player.queue.clear()

        embed = create_embed(
            title="Queue Cleared",
            description=(
                "The queue has been cleared of all songs!\n\nIssued by:"
                f" {interaction.user.mention}"
            ),
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Clear(bot))

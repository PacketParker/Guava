import discord
import datetime
from typing import Literal
from discord import app_commands
from discord.ext import commands
from cogs.music import Music

from utils.config import create_embed


class Pause(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.describe(pause="TRUE to pause, FALSE to unpause")
    @app_commands.check(Music.create_player)
    async def pause(
        self, interaction: discord.Interaction, pause: Literal["TRUE", "FALSE"]
    ):
        "Pause or unpause the current song"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        if pause:
            await player.set_pause(pause=True)
            embed = create_embed(
                title=f"Music Paused ⏸️",
                description=(
                    f"**[{player.current.title}]({player.current.uri})** by"
                    f" {player.current.author}\n\nQueued by:"
                    f" {player.current.requester.mention}"
                ),
                thumbnail=player.current.artwork_url,
            )
            return await interaction.response.send_message(embed=embed)

        else:
            await player.set_pause(pause=False)
            embed = create_embed(
                title=f"Music Unpaused ▶️",
                description=(
                    f"**[{player.current.title}]({player.current.uri})** by"
                    f" {player.current.author}\n\nQueued by:"
                    f" {player.current.requester.mention}"
                ),
                thumbnail=player.current.artwork_url,
            )
            return await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Pause(bot))

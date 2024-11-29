import discord
import datetime
from discord import app_commands
from discord.ext import commands
from cogs.music import Music
from typing import Literal

from utils.ai_recommendations import add_song_recommendations
from utils.config import create_embed


class Autoplay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.check(Music.create_player)
    @app_commands.describe(toggle="Turn autoplay ON or OFF")
    async def autoplay(
        self, interaction: discord.Interaction, toggle: Literal["ON", "OFF"]
    ):
        "Keep music playing 24/7 with AI-generated song recommendations"
        if toggle == "OFF":
            self.bot.autoplay.remove(interaction.guild.id)

            embed = create_embed(
                title="Autoplay Off",
                description=(
                    "Autoplay has been turned off. Song recommendations will"
                    " no longer be added to the queue."
                ),
            )
            return await interaction.response.send_message(embed=embed)

        # Otherwise, toggle must be "ON", so enable autoplaying

        if interaction.guild.id in self.bot.autoplay:
            embed = create_embed(
                title="Autoplay Already Enabled",
                description=(
                    "Autoplay is already enabled. If you would like to turn it"
                    " off, run </autoplay:1228216490386391052> and choose the"
                    " `OFF` option."
                ),
            )
            return await interaction.response.send_message(
                embed=embed, ephemeral=True
            )

        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        if len(player.queue) < 5:
            embed = create_embed(
                title="Not Enough Context",
                description=(
                    "Autoplay requires at least 5 songs in the queue in order"
                    " to generate recommendations. Please add more and try"
                    " again."
                ),
            )
            return await interaction.response.send_message(
                embed=embed, ephemeral=True
            )

        inputs = {}
        for song in player.queue[:10]:
            inputs[song.title] = song.author

        embed = create_embed(
            title="Getting AI Recommendations",
            description=(
                "Attempting to generate recommendations based on the current"
                " songs in your queue. Just a moment..."
            ),
        )
        await interaction.response.send_message(embed=embed)

        if await add_song_recommendations(
            self.bot.openai, self.bot.user, player, 5, inputs
        ):
            self.bot.autoplay.append(interaction.guild.id)
            embed = create_embed(
                title=":infinity: Autoplay Enabled :infinity:",
                description=(
                    "Recommendations have been generated and added to the"
                    " queue. Autoplay will automatically search for more"
                    " songs whenever the queue gets low.\n\nEnabled by:"
                    f" {interaction.user.mention}"
                ),
            )
            await interaction.edit_original_response(embed=embed)

        else:
            embed = create_embed(
                title="Autoplay Error",
                description=(
                    "Unable to get AI recommendations at this time. Please try"
                    " again. If issues continue, please fill out a bug report"
                    " with </bug:1224840889906499626>."
                ),
            )
            await interaction.edit_original_response(embed=embed)


async def setup(bot):
    await bot.add_cog(Autoplay(bot))

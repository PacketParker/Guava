import discord
from discord import app_commands
from discord.ext.commands.errors import *
import datetime

from utils.config import BOT_COLOR
from utils.custom_sources import LoadError


# Create a custom AppCommandError for the create_player function
class CheckPlayerError(app_commands.AppCommandError):
    def __init__(self, info):
        self.info = info


class Tree(app_commands.CommandTree):
    async def on_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ):
        music_commands = [
            "play",
            "clear",
            "np",
            "pause",
            "queue",
            "remove",
            "resume",
            "shuffle",
            "skip",
            "stop",
        ]

        if isinstance(error, CommandNotFound):
            return

        # Custom Error class for the `create_player` function
        # Issues that arise may be user not in vc, user not in correct vc, missing perms, etc.
        elif isinstance(error, CheckPlayerError):
            embed = discord.Embed(
                title=error.info["title"],
                description=error.info["description"],
                color=BOT_COLOR,
            )
            embed.set_footer(
                text=datetime.datetime.now(datetime.timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                + " UTC"
            )
            try:
                await interaction.response.send_message(
                    embed=embed, ephemeral=True
                )
            except discord.errors.InteractionResponded:
                await interaction.followup.send(embed=embed, ephemeral=True)

        # If `create_player` fails to create a player and fails
        # to raise a `CheckPlayerError`, this will catch it
        elif (
            isinstance(error, app_commands.CheckFailure)
            and interaction.command.name in music_commands
        ):
            embed = discord.Embed(
                title="Player Creation Error",
                description=(
                    "An error occured when trying to create a player. Please"
                    " submit a bug report with </bug:1224840889906499626> if"
                    " this issue persists."
                ),
                color=BOT_COLOR,
            )
            embed.set_footer(
                text=datetime.datetime.now(datetime.timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                + " UTC"
            )
            try:
                await interaction.response.send_message(
                    embed=embed, ephemeral=True
                )
            except discord.errors.InteractionResponded:
                await interaction.followup.send(embed=embed, ephemeral=True)

        elif (error, LoadError):
            embed = discord.Embed(
                title="Load Error",
                description=(
                    "Apple Music and Spotify do not allow direct playing from"
                    " their websites, and I was unable to load a track on a"
                    " valid source. Please try again."
                ),
                color=BOT_COLOR,
            )
            # Only send the error if the interaction is still valid
            try:
                await interaction.response.send_message(
                    embed=embed, ephemeral=True
                )
            except discord.errors.InteractionResponded:
                pass

        else:
            raise error

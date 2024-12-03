import discord
from discord import app_commands
from discord.ext.commands.errors import *

from utils.config import create_embed
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
            embed = create_embed(
                title=error.info["title"],
                description=error.info["description"],
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
            embed = create_embed(
                title="Player Creation Error",
                description=(
                    "An error occured when trying to create a player. Please"
                    " submit a bug report with </bug:1224840889906499626> if"
                    " this issue persists."
                ),
            )
            try:
                await interaction.response.send_message(
                    embed=embed, ephemeral=True
                )
            except discord.errors.InteractionResponded:
                await interaction.followup.send(embed=embed, ephemeral=True)

        else:
            raise error

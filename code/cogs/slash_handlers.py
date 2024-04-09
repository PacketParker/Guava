import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands.errors import *
import datetime

from global_variables import BOT_COLOR
from custom_source import LoadError


class slash_handlers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.tree.on_error = self.on_error

    async def on_error(self, interaction: discord.Interaction, error):
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

        # elif isinstance(error, app_commands.MissingPermissions):
        #     embed = discord.Embed(
        #         title="Missing Permissions!",
        #         description=f"{error}",
        #         color=BOT_COLOR
        #     )
        #     await interaction.response.send_message(embed=embed, ephemeral=True)

        # elif isinstance(error, app_commands.BotMissingPermissions):
        #     embed = discord.Embed(
        #         title="Bot Missing Permissions!",
        #         description=f"{error}",
        #         color=BOT_COLOR
        #     )
        #     await interaction.response.send_message(embed=embed, ephemeral=True)

        elif isinstance(error, app_commands.AppCommandError):
            embed = discord.Embed(
                title=error.args[0]["title"],
                description=error.args[0]["description"],
                color=BOT_COLOR,
            )
            embed.set_footer(
                text=datetime.datetime.now(datetime.timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                + " UTC"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif (
            isinstance(error, app_commands.CheckFailure)
            and interaction.command.name in music_commands
        ):
            embed = discord.Embed(
                title="Player Creation Error",
                description="An error occured when creating a player. Please try again.",
                color=BOT_COLOR,
            )
            embed.set_footer(
                text=datetime.datetime.now(datetime.timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                + " UTC"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif isinstance(error, LoadError):
            embed = discord.Embed(
                title="Nothing Found",
                description="Spotify does not allow direct play, meaning songs have to be found on a supported provider. In this case, the song couldn't be found. Please try again with a different song, or try searching for just the name and artist manually rather than sending a link.",
                color=BOT_COLOR,
            )
            embed.set_footer(
                text=datetime.datetime.now(datetime.timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                + " UTC"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            raise error

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        return


async def setup(bot: commands.Bot):
    await bot.add_cog(slash_handlers(bot))

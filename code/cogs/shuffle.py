import discord
import datetime
from discord import app_commands
from discord.ext import commands
from cogs.music import Music

from global_variables import BOT_COLOR


class Shuffle(commands.GroupCog, name="shuffle"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="on")
    @app_commands.check(Music.create_player)
    async def shuffle_on(self, interaction: discord.Interaction):
        "Play songs from the queue in a randomized order"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        player.shuffle = True

        embed = discord.Embed(
            title=f"Shuffle Enabled 🔀",
            description=f"All music will now be shuffled.",
            color=BOT_COLOR,
        )
        embed.set_footer(
            text=datetime.datetime.now(datetime.timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            + " UTC"
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="off")
    @app_commands.check(Music.create_player)
    async def shuffle_off(self, interaction: discord.Interaction):
        "Stop playing songs from queue in a randomized order"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        player.shuffle = False

        embed = discord.Embed(
            title=f"Disabled 🔀",
            description=f"Music will no longer be shuffled.",
            color=BOT_COLOR,
        )
        embed.set_footer(
            text=datetime.datetime.now(datetime.timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            + " UTC"
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Shuffle(bot))

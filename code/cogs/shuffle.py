import discord
import datetime
from discord import app_commands
from discord.ext import commands
from cogs.music import Music

from utils.config import create_embed


class Shuffle(commands.GroupCog, name="shuffle"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="on")
    @app_commands.check(Music.create_player)
    async def shuffle_on(self, interaction: discord.Interaction):
        "Play songs from the queue in a randomized order"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        player.shuffle = True

        embed = create_embed(
            title="Shuffle Enabled 🔀",
            description="All music will now be shuffled.",
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="off")
    @app_commands.check(Music.create_player)
    async def shuffle_off(self, interaction: discord.Interaction):
        "Stop playing songs from queue in a randomized order"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        player.shuffle = False

        embed = create_embed(
            title="Shuffle Disabled 🔀",
            description="Music will no longer be shuffled.",
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Shuffle(bot))

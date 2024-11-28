import discord
import datetime
from discord import app_commands
from discord.ext import commands
from cogs.music import Music

from utils.config import create_embed


class Repeat(commands.GroupCog, name="repeat"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="off")
    @app_commands.check(Music.create_player)
    async def repeat_off(self, interaction: discord.Interaction):
        "Turn song/queue repetition off"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        if player.loop == 0:
            embed = create_embed(
                title="Repeating Already Off",
                description="Music repetition is already turned off.",
            )
            return await interaction.response.send_message(
                embed=embed, ephemeral=True
            )

        player.loop = 0

        embed = create_embed(
            title="Repeating Off",
            description="Music will no longer be repeated.",
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="song")
    @app_commands.check(Music.create_player)
    async def repeat_song(self, interaction: discord.Interaction):
        "Forever repeat that song that is currently playing"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        if player.loop == 1:
            embed = create_embed(
                title="Repeating Already On",
                description="The current song is already being repeated.",
            )
            return await interaction.response.send_message(
                embed=embed, ephemeral=True
            )

        player.loop = 1
        embed = create_embed(
            title="Repeating Current Song 🔁",
            description=(
                "The song that is currently playing will be repeated until"
                " the </repeat off:1224840891395608737> command is run"
            ),
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="queue")
    @app_commands.check(Music.create_player)
    async def repeat_queue(self, interaction: discord.Interaction):
        "Continuously repeat the queue once it reaches the end"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        if player.loop == 2:
            embed = create_embed(
                title="Repeating Already On",
                description="The queue is already being repeated.",
            )
            return await interaction.response.send_message(
                embed=embed, ephemeral=True
            )

        player.loop = 2
        embed = create_embed(
            title="Repeating Queue 🔂",
            description=(
                "The queue will continuously repeat until the"
                " </repeat off:1224840891395608737> command is run."
            ),
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Repeat(bot))

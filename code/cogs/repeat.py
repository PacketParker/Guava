import discord
import datetime
from discord import app_commands
from discord.ext import commands
from cogs.music import Music

from config import BOT_COLOR


class Repeat(commands.GroupCog, name="repeat"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="off")
    @app_commands.check(Music.create_player)
    async def repeat_off(self, interaction: discord.Interaction):
        "Turn song/queue repetition off"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        if player.loop == 0:
            embed = discord.Embed(
                title=f"Repeating Already Off",
                description=f"Music repetition is already turned off.",
                color=BOT_COLOR,
            )
            embed.set_footer(
                text=datetime.datetime.now(datetime.timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                + " UTC"
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        player.loop = 0

        embed = discord.Embed(
            title=f"Repeating Off",
            description=f"Music will no longer be repeated.",
            color=BOT_COLOR,
        )
        embed.set_footer(
            text=datetime.datetime.now(datetime.timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            + " UTC"
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="song")
    @app_commands.check(Music.create_player)
    async def repeat_song(self, interaction: discord.Interaction):
        "Forever repeat that song that is currently playing"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        if player.loop == 1:
            embed = discord.Embed(
                title=f"Repeating Already On",
                description=f"The current song is already being repeated.",
                color=BOT_COLOR,
            )
            embed.set_footer(
                text=datetime.datetime.now(datetime.timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                + " UTC"
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        player.loop = 1

        embed = discord.Embed(
            title=f"Repeating Current Song 🔁",
            description=f"The song that is currently playing will be repeated until the `/repeat off` command is run",
            color=BOT_COLOR,
        )
        embed.set_footer(
            text=datetime.datetime.now(datetime.timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            + " UTC"
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="queue")
    @app_commands.check(Music.create_player)
    async def repeat_queue(self, interaction: discord.Interaction):
        "Continuously repeat the queue once it reaches the end"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        if player.loop == 2:
            embed = discord.Embed(
                title=f"Repeating Already On",
                description=f"The queue is already being repeated.",
                color=BOT_COLOR,
            )
            embed.set_footer(
                text=datetime.datetime.now(datetime.timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                + " UTC"
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        player.loop = 2

        embed = discord.Embed(
            title=f"Repeating Current Song 🔂",
            description=f"All songs in the queue will continue to repeat until the `/repeat off` command is run.",
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
    await bot.add_cog(Repeat(bot))

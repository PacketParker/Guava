import discord
import datetime
from discord import app_commands
from discord.ext import commands
from cogs.music import Music

from utils.config import BOT_COLOR


class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.check(Music.create_player)
    async def lyrics(self, interaction: discord.Interaction):
        "Get lyrics for the song that is currently playing"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        # If the Genius API client is not setup, send an error message
        if not self.bot.genius:
            embed = discord.Embed(
                title="Lyrics Feature Error",
                description=(
                    "The lyrics feature is currently disabled due to errors"
                    " with the Genius API."
                ),
                color=BOT_COLOR,
            )
            embed.set_footer(
                text=datetime.datetime.now(datetime.timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                + " UTC"
            )
            return await interaction.response.send_message(
                embed=embed, ephemeral=True
            )

        # Defer the interaction to avoid getting 404 Not Found errors
        # if fetching the lyrics takes a long time
        await interaction.response.defer(ephemeral=True)

        # Search for the songs lyrics with Genius
        song = self.bot.genius.search_song(
            player.current.title, player.current.author
        )

        # If no lyrics are found, send an error message
        if song is None:
            embed = discord.Embed(
                title="Lyrics Not Found",
                description=(
                    "Unfortunately, I wasn't able to find any lyrics for the"
                    " song that is currently playing."
                ),
                color=BOT_COLOR,
            )
            embed.set_thumbnail(url=player.current.artwork_url)
            embed.set_footer(
                text=datetime.datetime.now(datetime.timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                + " UTC"
            )
            return await interaction.edit_original_response(embed=embed)

        # Remove unwanted text
        lyrics = song.lyrics
        lyrics = lyrics.split(" Lyrics", 1)[-1]
        lyrics = lyrics.replace("You might also like", "\n")
        lyrics = lyrics[:-7]

        # If the lyrics are too long, send just a link to the lyrics
        if len(lyrics) > 2048:
            embed = discord.Embed(
                title=(
                    f"Lyrics for {player.current.title} by"
                    f" {player.current.author}"
                ),
                description=(
                    "Song lyrics are too long to display on Discord. [Click"
                    f" here to view the lyrics on Genius]({song.url})."
                ),
                color=BOT_COLOR,
            )
            embed.set_thumbnail(url=player.current.artwork_url)
            embed.set_footer(
                text=datetime.datetime.now(datetime.timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                + " UTC"
            )
            return await interaction.edit_original_response(embed=embed)

        # If everything is successful, send the lyrics
        embed = discord.Embed(
            title=(
                f"Lyrics for {player.current.title} by {player.current.author}"
            ),
            description=f"Provided from [Genius]({song.url})\n\n" + lyrics,
            color=BOT_COLOR,
        )
        embed.set_thumbnail(url=player.current.artwork_url)
        embed.set_footer(
            text=datetime.datetime.now(datetime.timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            + " UTC"
        )
        await interaction.edit_original_response(embed=embed)


async def setup(bot):
    await bot.add_cog(Lyrics(bot))

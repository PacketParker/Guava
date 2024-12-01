import discord
import datetime
from discord import app_commands
from discord.ext import commands
from lavalink import LoadType
import re

from cogs.music import Music, LavalinkVoiceClient
from utils.config import YOUTUBE_SUPPORT, create_embed
from utils.custom_sources import (
    LoadError,
    CustomAudioTrack,
)
from utils.source_helpers.parse import parse_custom_source


url_rx = re.compile(r"https?://(?:www\.)?.+")


class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.check(Music.create_player)
    @app_commands.describe(query="Name or link of song")
    async def play(self, interaction: discord.Interaction, query: str):
        "Play a song from your favorite music provider"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        # Notify users that YouTube links are not allowed if YouTube support is disabled
        if "youtube.com" in query or "youtu.be" in query:
            if not YOUTUBE_SUPPORT:
                embed = create_embed(
                    title="YouTube Not Supported",
                    description=(
                        "Unfortunately, YouTube does not allow bots to stream"
                        " from their platform. Try sending a link for a"
                        " different platform, or simply type the name of the"
                        " song and I will automatically find it on a supported"
                        " platform."
                    ),
                )
                return await interaction.response.send_message(
                    embed=embed, ephemeral=True
                )

        # Check for custom sources (Apple Music/Spotify)
        if "music.apple.com" in query:
            results, embed = await parse_custom_source(
                self, "apple", query, interaction.user
            )

        elif "open.spotify.com" in query:
            results, embed = await parse_custom_source(
                self, "spotify", query, interaction.user
            )

        # For anything else, use default Lavalink providers to search the query
        else:
            # If the query is not a URL, begin searching
            if not url_rx.match(query):
                dzsearch = f"dzsearch:{query}"
                results = await player.node.get_tracks(dzsearch)
                # If Deezer returned nothing
                if not results.tracks or results.load_type in (
                    LoadType.EMPTY,
                    LoadType.ERROR,
                ):
                    if YOUTUBE_SUPPORT:
                        ytmsearch = f"ytmsearch:{query}"
                        results = await player.node.get_tracks(ytmsearch)
                        # If YouTube Music returned nothing
                        if not results.tracks or results.load_type in (
                            LoadType.EMPTY,
                            LoadType.ERROR,
                        ):
                            # Final search attempt with YouTube
                            ytsearch = f"ytsearch:{query} audio"
                            results = await player.node.get_tracks(ytsearch)
            else:
                results = await player.node.get_tracks(query)

            # If there are no results found, set results/embed to None, handled further down
            if not results.tracks or results.load_type in (
                LoadType.EMPTY,
                LoadType.ERROR,
            ):
                results, embed = None, None

            # Create the embed if the results are a playlist
            if results.load_type == LoadType.PLAYLIST:
                embed = create_embed(
                    title="Songs Queued",
                    description=(
                        f"**{results.playlist_info.name}**\n"
                        f"` {len(results.tracks)} ` tracks\n\n"
                        f"Queued by: {interaction.user.mention}"
                    ),
                )
            # Otherwise, the result is just a single track, create that embed
            else:
                # Remove all but first track (most relevant result)
                results.tracks = results.tracks[:1]
                embed = create_embed(
                    title="Song Queued",
                    description=(
                        f"**{results.tracks[0].title}** by"
                        f" **{results.tracks[0].author}**\n\nQueued by:"
                        f" {interaction.user.mention}"
                    ),
                    thumbnail=results.tracks[0].artwork_url,
                )

        # If there are no results, and no embed
        if not results and not embed:
            embed = create_embed(
                title="Nothing Found",
                description=(
                    "No songs were found for that query. Please try again and"
                    " fill out a bug report with </bug:1224840889906499626> if"
                    " this continues to happen."
                ),
            )
            return await interaction.response.send_message(
                embed=embed, ephemeral=True
            )
        # If there are no results, but there is an embed (error msg)
        elif embed and not results:
            return await interaction.response.send_message(
                embed=embed, ephemeral=True
            )
        # If there are results, add them to the player
        else:
            for track in results.tracks:
                player.add(requester=interaction.user, track=track)

            # If the track is CustomAudioTrack (Apple Music/Spotify)
            if type(results.tracks[0]) == CustomAudioTrack:
                # Attempt to load an actual track from a provider
                try:
                    await results.tracks[0].load(player.node)
                # If it fails, remove it from the queue and alert the user
                except LoadError as e:
                    player.queue.remove(results.tracks[0])
                    embed = create_embed(
                        title="Load Error",
                        description=(
                            "Apple Music and Spotify do not allow direct"
                            " playing from their websites, and I was unable to"
                            " load a track on a supported platform. Please try"
                            " again."
                        ),
                    )
                    return await interaction.response.send_message(
                        embed=embed, ephemeral=True
                    )

            # Join the voice channel if not already connected
            if not interaction.guild.voice_client:
                await interaction.user.voice.channel.connect(
                    cls=LavalinkVoiceClient, self_deaf=True
                )

            # Only call player.play if it is not already playing, otherwise it will
            # effectively skip the current track
            if not player.is_playing:
                await player.play()

            await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Play(bot))

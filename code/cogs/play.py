import discord
import datetime
from discord import app_commands
from discord.ext import commands
from cogs.music import Music
from lavalink import LoadType
import re
from cogs.music import LavalinkVoiceClient
import requests

from global_variables import BOT_COLOR
from custom_source import CustomSource


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

        # Notify users that YouTube and Apple Music links are not allowed

        if "youtube.com" in query or "youtu.be" in query:
            embed = discord.Embed(
                title="YouTube Not Supported",
                description="Unfortunately, YouTube does not allow bots to stream from their platform. Try sending a link for a different platform, or simply type the name of the song and I will automatically find it on a supported platform.",
                color=BOT_COLOR,
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        if "music.apple.com" in query:
            embed = discord.Embed(
                title="Apple Music Not Supported",
                description="Unfortunately, Apple Music does not allow bots to stream from their platform. Try sending a link for a different platform, or simply type the name of the song and I will automatically find it on a supported platform.",
                color=BOT_COLOR,
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        # If a Spotify link is found, act accordingly
        # We use a custom source for this (I tried the LavaSrc plugin, but Spotify
        # links would just result in random shit being played whenever ytsearch was removed)
        if "open.spotify.com" in query:
            embed = discord.Embed(color=BOT_COLOR)

            if "open.spotify.com/playlist" in query:
                playlist_id = query.split("playlist/")[1].split("?si=")[0]
                playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
                response = requests.get(playlist_url, headers=self.bot.spotify_headers)
                if response.status_code == 200:
                    playlist = response.json()

                    embed.title = "Playlist Queued"
                    embed.description = f"**{playlist['name']}** from **{playlist['owner']['display_name']}**\n` {len(playlist['tracks']['items'])} ` tracks\n\nQueued by: {interaction.user.mention}"
                    embed.set_thumbnail(url=playlist["images"][0]["url"])
                    embed.set_footer(
                        text=datetime.datetime.now(datetime.timezone.utc).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        + " UTC"
                    )
                    await interaction.response.send_message(embed=embed)

                    tracks = await CustomSource.load_playlist(
                        self, interaction.user, playlist
                    )
                    for track in tracks["tracks"]:
                        player.add(requester=interaction.user, track=track)

            if "open.spotify.com/album" in query:
                album_id = query.split("album/")[1]
                album_url = f"https://api.spotify.com/v1/albums/{album_id}"
                response = requests.get(album_url, headers=self.bot.spotify_headers)
                if response.status_code == 200:
                    album = response.json()

                    embed.title = "Album Queued"
                    embed.description = f"**{album['name']}** by **{album['artists'][0]['name']}**\n` {len(album['tracks']['items'])} ` tracks\n\nQueued by: {interaction.user.mention}"
                    embed.set_thumbnail(url=album["images"][0]["url"])
                    embed.set_footer(
                        text=datetime.datetime.now(datetime.timezone.utc).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        + " UTC"
                    )
                    await interaction.response.send_message(embed=embed)

                    tracks = await CustomSource.load_album(
                        self, interaction.user, album
                    )
                    for track in tracks["tracks"]:
                        player.add(requester=interaction.user, track=track)

            if "open.spotify.com/track" in query:
                track_id = query.split("track/")[1]
                track_url = f"https://api.spotify.com/v1/tracks/{track_id}"
                response = requests.get(track_url, headers=self.bot.spotify_headers)
                if response.status_code == 200:
                    track = response.json()

                    embed.title = "Track Queued"
                    embed.description = f"**{track['name']}** by **{track['artists'][0]['name']}**\n\nQueued by: {interaction.user.mention}"
                    embed.set_thumbnail(url=track["album"]["images"][0]["url"])
                    embed.set_footer(
                        text=datetime.datetime.now(datetime.timezone.utc).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        + " UTC"
                    )
                    await interaction.response.send_message(embed=embed)

                    results = await CustomSource.load_item(
                        self, interaction.user, track
                    )
                    player.add(requester=interaction.user, track=results.tracks[0])

            if "open.spotify.com/artists" in query:
                embed.title = "Artists Cannot Be Played"
                embed.description = "I cannot play just artists, you must provide a song/album/playlist. Please try again."
                return await interaction.response.send_message(
                    embed=embed, ephemeral=True
                )

        # For anything else, do default searches and attempt to find track and play

        else:
            if not url_rx.match(query):
                ytsearch = f"ytsearch:{query}"
                results = await player.node.get_tracks(ytsearch)

                if not results.tracks or results.load_type in (
                    LoadType.EMPTY,
                    LoadType.ERROR,
                ):
                    dzsearch = f"dzsearch:{query}"
                    results = await player.node.get_tracks(dzsearch)
            else:
                results = await player.node.get_tracks(query)

            embed = discord.Embed(color=BOT_COLOR)

            if not results.tracks or results.load_type in (
                LoadType.EMPTY,
                LoadType.ERROR,
            ):
                embed.title = "Nothing Found"
                embed.description = "Nothing for that query could be found. If this continues happening for other songs, please run </bug:1224840889906499626> to let the developer know."
                return await interaction.response.send_message(
                    embed=embed, ephemeral=True
                )

            elif results.load_type == LoadType.PLAYLIST:
                tracks = results.tracks

                for track in tracks:
                    player.add(requester=interaction.user, track=track)

                embed.title = "Songs Queued!"
                embed.description = f"**{results.playlist_info.name}**\n` {len(tracks)} ` tracks\n\nQueued by: {interaction.user.mention}"
                embed.set_footer(
                    text=datetime.datetime.now(datetime.timezone.utc).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    + " UTC"
                )
                await interaction.response.send_message(embed=embed)

            else:
                track = results.tracks[0]
                player.add(requester=interaction.user, track=track)

                embed.title = "Track Queued"
                embed.description = f"**{track.title}** by **{track.author}**\n\nQueued by: {interaction.user.mention}"
                embed.set_thumbnail(url=track.artwork_url)
                embed.set_footer(
                    text=datetime.datetime.now(datetime.timezone.utc).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    + " UTC"
                )
                await interaction.response.send_message(embed=embed)

        # Only join the voice channel now, so that the bot doesn't join if nothing is found
        if not interaction.guild.voice_client:
            await interaction.user.voice.channel.connect(
                cls=LavalinkVoiceClient, self_deaf=True
            )

        # We don't want to call .play() if the player is playing as that will
        # effectively skip the current track
        if not player.is_playing:
            await player.play()


async def setup(bot):
    await bot.add_cog(Play(bot))

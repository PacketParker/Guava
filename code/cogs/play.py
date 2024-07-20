import discord
import datetime
from discord import app_commands
from discord.ext import commands
from lavalink import LoadType
import re
import requests

from cogs.music import Music, LavalinkVoiceClient
from utils.config import BOT_COLOR, APPLE_MUSIC_KEY
from utils.custom_sources import SpotifySource, AppleSource


url_rx = re.compile(r"https?://(?:www\.)?.+")

apple_headers = {
    "Authorization": f"Bearer {APPLE_MUSIC_KEY}",
    "Origin": "https://apple.com",
}


class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.check(Music.create_player)
    @app_commands.describe(query="Name or link of song")
    async def play(self, interaction: discord.Interaction, query: str):
        "Play a song from your favorite music provider"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        # Notify users that YouTube links are not allowed

        if "youtube.com" in query or "youtu.be" in query:
            embed = discord.Embed(
                title="YouTube Not Supported",
                description="Unfortunately, YouTube does not allow bots to stream from their platform. Try sending a link for a different platform, or simply type the name of the song and I will automatically find it on a supported platform.",
                color=BOT_COLOR,
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        ###
        ### APPLE MUSIC links, perform API requests and load all tracks from the playlist/album/track
        ###

        if "music.apple.com" in query:
            embed = discord.Embed(color=BOT_COLOR)

            if "/playlist/" in query and "?i=" not in query:
                playlist_id = query.split("/playlist/")[1].split("/")[1]
                # Get all of the tracks in the playlist (limit at 250)
                playlist_url = f"https://api.music.apple.com/v1/catalog/us/playlists/{playlist_id}/tracks?limit=100"
                response = requests.get(playlist_url, headers=apple_headers)
                if response.status_code == 200:
                    playlist = response.json()
                    # Get the general playlist info (name, artwork)
                    playlist_info_url = f"https://api.music.apple.com/v1/catalog/us/playlists/{playlist_id}"
                    playlist_info = requests.get(playlist_info_url, headers=apple_headers)
                    playlist_info = playlist_info.json()
                    try:
                        artwork_url = playlist_info["data"][0]["attributes"]["artwork"]["url"].replace(
                            "{w}x{h}", "300x300"
                        )
                    except KeyError:
                        artwork_url = None

                    embed.title = "Playlist Queued"
                    embed.description = f"**{playlist_info['data'][0]['attributes']['name']}**\n` {len(playlist['data'])} ` tracks\n\nQueued by: {interaction.user.mention}"
                    embed.set_thumbnail(url=artwork_url)
                    embed.set_footer(
                        text=datetime.datetime.now(datetime.timezone.utc).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        + " UTC"
                    )
                    # Add small alert if the playlist is the max size
                    if len(playlist["data"]) == 100:
                        embed.description += "\n\n*This playlist is longer than the 100 song maximum. Only the first 100 songs will be queued.*"

                    await interaction.response.send_message(embed=embed)

                    tracks = await AppleSource.load_playlist(
                        self, interaction.user, playlist
                    )
                    for track in tracks["tracks"]:
                        player.add(requester=interaction.user, track=track)

            # If there is an album, not a specific song within the album
            if "/album/" in query and "?i=" not in query:
                album_id = query.split("/album/")[1].split("/")[1]
                album_url = f"https://api.music.apple.com/v1/catalog/us/albums/{album_id}"
                response = requests.get(album_url, headers=apple_headers)
                if response.status_code == 200:
                    album = response.json()

                    embed.title = "Album Queued"
                    embed.description = f"**{album['data'][0]['attributes']['name']}** by **{album['data'][0]['attributes']['artistName']}**\n` {len(album['data'][0]['relationships']['tracks']['data'])} ` tracks\n\nQueued by: {interaction.user.mention}"
                    embed.set_thumbnail(
                        url=album["data"][0]["attributes"]["artwork"]["url"].replace(
                            "{w}x{h}", "300x300"
                        )
                    )
                    embed.set_footer(
                        text=datetime.datetime.now(datetime.timezone.utc).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        + " UTC"
                    )
                    await interaction.response.send_message(embed=embed)

                    tracks = await AppleSource.load_album(self, interaction.user, album)
                    for track in tracks["tracks"]:
                        player.add(requester=interaction.user, track=track)

            # If there is a specific song
            if "/album/" in query and "?i=" in query:
                song_id = query.split("/album/")[1].split("?i=")[1]
                song_url = f"https://api.music.apple.com/v1/catalog/us/songs/{song_id}"
                response = requests.get(song_url, headers=apple_headers)
                if response.status_code == 200:
                    song = response.json()

                    embed.title = "Song Queued"
                    embed.description = f"**{song['data'][0]['attributes']['name']}** by **{song['data'][0]['attributes']['artistName']}**\n\nQueued by: {interaction.user.mention}"
                    embed.set_thumbnail(
                        url=song["data"][0]["attributes"]["artwork"]["url"].replace(
                            "{w}x{h}", "300x300"
                        )
                    )
                    embed.set_footer(
                        text=datetime.datetime.now(datetime.timezone.utc).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        + " UTC"
                    )
                    await interaction.response.send_message(embed=embed)

                    results = await AppleSource.load_item(self, interaction.user, song)
                    player.add(requester=interaction.user, track=results.tracks[0])

        ###
        ### SPOTIFY links, perform API requests and load all tracks from the playlist/album/track
        ###

        elif "open.spotify.com" in query:
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

                    tracks = await SpotifySource.load_playlist(
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

                    tracks = await SpotifySource.load_album(
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

                    results = await SpotifySource.load_item(
                        self, interaction.user, track
                    )
                    player.add(requester=interaction.user, track=results.tracks[0])

            if "open.spotify.com/artists" in query:
                embed.title = "Artists Cannot Be Played"
                embed.description = "I cannot play just artists, you must provide a song/album/playlist. Please try again."
                return await interaction.response.send_message(
                    embed=embed, ephemeral=True
                )

        ###
        ### For anything else, use default Lavalink providers to search the query
        ###

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

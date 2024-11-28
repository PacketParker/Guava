import discord

from utils.source_helpers.apple import (
    album as apple_album,
    playlist as apple_playlist,
    song as apple_song,
)
from utils.source_helpers.spotify import (
    album as spotify_album,
    playlist as spotify_playlist,
    song as spotify_song,
)
from utils.custom_sources import AppleSource, SpotifySource


async def parse_custom_source(
    self, provider: str, query: str, user: discord.User
):
    """
    Parse the query and run the appropriate functions to get the results/info

    Return the results and an embed or None, None
    """
    load_funcs = {
        "apple": {
            "album": apple_album.load,
            "playlist": apple_playlist.load,
            "song": apple_song.load,
        },
        "spotify": {
            "album": spotify_album.load,
            "playlist": spotify_playlist.load,
            "song": spotify_song.load,
        },
    }

    headers = {
        "apple": self.bot.apple_headers,
        "spotify": self.bot.spotify_headers,
    }

    sources = {
        "apple": AppleSource,
        "spotify": SpotifySource,
    }

    # Catch all songs
    if "?i=" in query or "/track/" in query:
        song, embed = await load_funcs[provider]["song"](
            headers[provider], query, user
        )

        if song:
            results = await sources[provider].load_item(self, user, song)
        else:
            return None, embed
    # Catch all playlists
    elif "/playlist/" in query:
        playlist, embed = await load_funcs[provider]["playlist"](
            headers[provider], query, user
        )

        if playlist:
            results = await sources[provider].load_playlist(
                self, user, playlist
            )
        else:
            return None, embed
    # Catch all albums
    elif "/album/" in query:
        album, embed = await load_funcs[provider]["album"](
            headers[provider], query, user
        )

        if album:
            results = await sources[provider].load_album(self, user, album)
        else:
            return None, embed

    return results, embed

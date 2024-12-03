from lavalink import (
    LoadResult,
    LoadType,
    Source,
    DeferredAudioTrack,
    PlaylistInfo,
)

from utils.config import YOUTUBE_SUPPORT


class LoadError(
    Exception
):  # We'll raise this if we have trouble loading our track.
    pass


"""
Retrieve the playback URL for a custom track
"""


class CustomAudioTrack(DeferredAudioTrack):
    # A DeferredAudioTrack allows us to load metadata now, and a playback URL later.
    # This makes the DeferredAudioTrack highly efficient, particularly in cases
    # where large playlists are loaded.

    async def load(
        self, client
    ):  # Load our 'actual' playback track using the metadata from this one.
        dzsearch = f"dzsearch:{self.title} {self.author}"
        results = await client.get_tracks(dzsearch)
        if not results.tracks or results.load_type in (
            LoadType.EMPTY,
            LoadType.ERROR,
        ):
            if YOUTUBE_SUPPORT:
                ytmsearch = f"ytmsearch:{self.title} {self.author}"
                results = await client.get_tracks(ytmsearch)

                if not results.tracks or results.load_type in (
                    LoadType.EMPTY,
                    LoadType.ERROR,
                ):
                    ytsearch = f"ytsearch:{self.title} {self.author} audio"
                    results = await client.get_tracks(ytsearch)

                    if not results.tracks or results.load_type in (
                        LoadType.EMPTY,
                        LoadType.ERROR,
                    ):
                        raise LoadError

        first_track = results.tracks[
            0
        ]  # Grab the first track from the results.
        base64 = first_track.track  # Extract the base64 string from the track.
        self.track = base64  # We'll store this for later, as it allows us to save making network requests
        # if this track is re-used (e.g. repeat).

        return base64


"""
Custom Source for Spotify links
"""


class SpotifySource(Source):
    def __init__(self):
        super().__init__(
            name="custom"
        )  # Initialising our custom source with the name 'custom'.

    async def load_item(self, user, metadata):
        try:
            artwork_url = metadata["album"]["images"][0]["url"]
        except IndexError:
            artwork_url = None
        track = CustomAudioTrack(
            {  # Create an instance of our CustomAudioTrack.
                "identifier": metadata[
                    "id"
                ],  # Fill it with metadata that we've obtained from our source's provider.
                "isSeekable": True,
                "author": metadata["artists"][0]["name"],
                "length": metadata["duration_ms"],
                "isStream": False,
                "title": metadata["name"],
                "uri": metadata["external_urls"]["spotify"],
                "duration": metadata["duration_ms"],
                "artworkUrl": artwork_url,
            },
            requester=user,
        )
        return LoadResult(
            LoadType.TRACK, [track], playlist_info=PlaylistInfo.none()
        )

    async def load_album(self, user, metadata):
        try:
            artwork_url = metadata["images"][0]["url"]
        except IndexError:
            artwork_url = None

        tracks = []
        for track in metadata["tracks"][
            "items"
        ]:  # Loop through each track in the album.
            tracks.append(
                CustomAudioTrack(
                    {  # Create an instance of our CustomAudioTrack.
                        "identifier": track[
                            "id"
                        ],  # Fill it with metadata that we've obtained from our source's provider.
                        "isSeekable": True,
                        "author": track["artists"][0]["name"],
                        "length": track["duration_ms"],
                        "isStream": False,
                        "title": track["name"],
                        "uri": track["external_urls"]["spotify"],
                        "duration": track["duration_ms"],
                        "artworkUrl": artwork_url,
                    },
                    requester=user,
                )
            )

        return LoadResult(
            LoadType.PLAYLIST, tracks, playlist_info=PlaylistInfo.none()
        )

    async def load_playlist(self, user, metadata):
        tracks = []
        for track in metadata["tracks"][
            "items"
        ]:  # Loop through each track in the playlist.
            try:
                artwork_url = track["track"]["album"]["images"][0]["url"]
            except IndexError:
                artwork_url = None
            tracks.append(
                CustomAudioTrack(
                    {  # Create an instance of our CustomAudioTrack.
                        "identifier": track["track"][
                            "id"
                        ],  # Fill it with metadata that we've obtained from our source's provider.
                        "isSeekable": True,
                        "author": track["track"]["artists"][0]["name"],
                        "length": track["track"]["duration_ms"],
                        "isStream": False,
                        "title": track["track"]["name"],
                        "uri": track["track"]["external_urls"]["spotify"],
                        "duration": track["track"]["duration_ms"],
                        "artworkUrl": artwork_url,
                    },
                    requster=user,
                )
            )

        return LoadResult(
            LoadType.PLAYLIST, tracks, playlist_info=PlaylistInfo.none()
        )

    async def load_artist(self, user, metadata):
        tracks = []
        for track in metadata["tracks"]:
            try:
                artwork_url = track["album"]["images"][0]["url"]
            except IndexError:
                artwork_url = None
            tracks.append(
                CustomAudioTrack(
                    {
                        "identifier": track["id"],
                        "isSeekable": True,
                        "author": track["artists"][0]["name"],
                        "length": track["duration_ms"],
                        "isStream": False,
                        "title": track["name"],
                        "uri": track["external_urls"]["spotify"],
                        "duration": track["duration_ms"],
                        "artworkUrl": artwork_url,
                    },
                    requester=user,
                )
            )

        return LoadResult(
            LoadType.PLAYLIST, tracks, playlist_info=PlaylistInfo.none()
        )


"""
Custom Source for Apple Music links
"""


class AppleSource(Source):
    def __init__(self):
        super().__init__(name="custom")

    async def load_item(self, user, metadata):
        track = CustomAudioTrack(
            {  # Create an instance of our CustomAudioTrack.
                "identifier": metadata["data"][0]["id"],
                "isSeekable": True,
                "author": metadata["data"][0]["attributes"]["artistName"],
                "length": metadata["data"][0]["attributes"][
                    "durationInMillis"
                ],
                "isStream": False,
                "title": metadata["data"][0]["attributes"]["name"],
                "uri": metadata["data"][0]["attributes"]["url"],
                "duration": metadata["data"][0]["attributes"][
                    "durationInMillis"
                ],
                "artworkUrl": metadata["data"][0]["attributes"]["artwork"][
                    "url"
                ].replace("{w}x{h}", "300x300"),
            },
            requester=user,
        )
        return LoadResult(
            LoadType.TRACK, [track], playlist_info=PlaylistInfo.none()
        )

    async def load_album(self, user, metadata):
        tracks = []
        for track in metadata["data"][0]["relationships"]["tracks"][
            "data"
        ]:  # Loop through each track in the album.
            tracks.append(
                CustomAudioTrack(
                    {  # Create an instance of our CustomAudioTrack.
                        "identifier": track["id"],
                        "isSeekable": True,
                        "author": track["attributes"]["artistName"],
                        "length": track["attributes"]["durationInMillis"],
                        "isStream": False,
                        "title": track["attributes"]["name"],
                        "uri": track["attributes"]["url"],
                        "duration": track["attributes"]["durationInMillis"],
                        "artworkUrl": track["attributes"]["artwork"][
                            "url"
                        ].replace("{w}x{h}", "300x300"),
                    },
                    requster=user,
                )
            )

        return LoadResult(
            LoadType.PLAYLIST, tracks, playlist_info=PlaylistInfo.none()
        )

    async def load_playlist(self, user, metadata):
        tracks = []
        for track in metadata[
            "data"
        ]:  # Loop through each track in the playlist.
            tracks.append(
                CustomAudioTrack(
                    {  # Create an instance of our CustomAudioTrack.
                        "identifier": track["id"],
                        "isSeekable": True,
                        "author": track["attributes"]["artistName"],
                        "length": track["attributes"]["durationInMillis"],
                        "isStream": False,
                        "title": track["attributes"]["name"],
                        "uri": track["attributes"]["url"],
                        "duration": track["attributes"]["durationInMillis"],
                        "artworkUrl": track["attributes"]["artwork"][
                            "url"
                        ].replace("{w}x{h}", "300x300"),
                    },
                    requster=user,
                )
            )

        return LoadResult(
            LoadType.PLAYLIST, tracks, playlist_info=PlaylistInfo.none()
        )

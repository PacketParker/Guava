import datetime
import discord
import requests
from typing import Tuple, Optional
from requests.exceptions import JSONDecodeError

from utils.config import create_embed, LOG


async def load(
    headers: dict,
    query: str,
    user: discord.User,
) -> Tuple[Optional[dict], Optional[discord.Embed]]:
    """
    Get the playlist info from the Spotify API
    """
    playlist_id = query.split("/playlist/")[1].split("?si=")[0]

    try:
        # Get the playlist info
        response = requests.get(
            f"https://api.spotify.com/v1/playlists/{playlist_id}",
            headers=headers,
        )

        if response.status_code == 404:
            embed = create_embed(
                title="Playlist Not Found",
                description=(
                    "The playlist could not be found as the provided link is"
                    " invalid. Please try again."
                ),
            )
            return None, embed

        if response.status_code == 401:
            LOG.error(
                "Could not authorize with Spotify API. Likely need to"
                " restart the bot."
            )
            return None, None

        response.raise_for_status()
        # Unpack the playlist info
        playlist = response.json()
        name = playlist["name"]
        owner = playlist["owner"]["display_name"]
        num_tracks = len(playlist["tracks"]["items"])
        artwork_url = playlist["images"][0]["url"]
    except IndexError:
        LOG.error("Failed unpacking Spotify playlist info")
        return None, None
    except (JSONDecodeError, requests.HTTPError):
        LOG.error("Failed making request to Spotify API")
        return None, None

    embed = create_embed(
        title="Playlist Queued",
        description=(
            f"**{name}** from **{owner}**\n"
            f"` {num_tracks} ` tracks\n\n"
            f"Queued by {user.mention}"
        ),
        thumbnail=artwork_url,
    )

    return playlist, embed

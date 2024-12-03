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
    Get the artists top tracks from the Spotify API
    """
    artist_id = query.split("/artist/")[1]

    try:
        # Get the artists songs
        response = requests.get(
            f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks",
            headers=headers,
        )

        if response.status_code == 404:
            embed = create_embed(
                title="Artist Not Found",
                description=(
                    "Either the provided link is malformed, the artist does"
                    " not exist, or the artist does not have any songs."
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
        # Unpack the artists songs
        artist = response.json()
        name = artist["tracks"][0]["artists"][0]["name"]
        num_tracks = len(artist["tracks"])

        # Get the artist info (for the thumbnail)
        response = requests.get(
            f"https://api.spotify.com/v1/artists/{artist_id}",
            headers=headers,
        )

        response.raise_for_status()
        try:
            artwork_url = response.json()["images"][0]["url"]
        except IndexError:
            artwork_url = None

    except IndexError:
        LOG.error("Failed unpacking Spotify artist info")
        return None, None
    except (JSONDecodeError, requests.HTTPError):
        LOG.error("Failed making request to Spotify API")
        return None, None

    embed = create_embed(
        title="Artist Queued",
        description=(
            f"Top `{num_tracks}` track by **{name}**\n\n"
            f"Queued by {user.mention}"
        ),
        thumbnail=artwork_url,
    )
    return artist, embed

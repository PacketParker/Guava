import datetime
import discord
import requests
from typing import Tuple, Optional
from requests.exceptions import JSONDecodeError

from utils.config import BOT_COLOR, LOG


async def load(
    headers: dict,
    query: str,
    user: discord.User,
) -> Tuple[Optional[dict], Optional[discord.Embed]]:
    """
    Get the playlist info from the Apple Music API
    """
    playlist_id = query.split("/playlist/")[1].split("/")[1]
    try:
        # Get all of the tracks in the playlist (limit at 100)
        response = requests.get(
            f"https://api.music.apple.com/v1/catalog/us/playlists/{playlist_id}/tracks?limit=100",
            headers=headers,
        )

        if response.status_code == 404:
            embed = discord.Embed(
                title="Playlist Not Found",
                description=(
                    "The playlist could not be found as the provided link is"
                    " invalid. Please try again."
                ),
                color=BOT_COLOR,
            )
            return None, embed

        if response.status_code == 401:
            LOG.error(
                "Could not authorize with Apple Music API. Likely need to"
                " restart the bot."
            )
            return None, None

        response.raise_for_status()
        playlist = response.json()

        # Get the general playlist info (name, artwork)
        response = requests.get(
            f"https://api.music.apple.com/v1/catalog/us/playlists/{playlist_id}",
            headers=headers,
        )

        response.raise_for_status()
        # Unpack the playlist info
        playlist_info = response.json()
        name = playlist_info["data"][0]["attributes"]["name"]
        num_tracks = len(playlist["data"])
    except IndexError:
        LOG.error("Failed unpacking Apple Music playlist info")
        return None, None
    except (JSONDecodeError, requests.HTTPError):
        LOG.error("Failed making request to Apple Music API")
        return None, None

    # Extract artwork URL, if available
    artwork_url = (
        playlist_info["data"][0]["attributes"]
        .get("artwork", {})
        .get("url", None)
    )
    if artwork_url:
        artwork_url = artwork_url.replace("{w}x{h}", "300x300")

    embed = discord.Embed(
        title="Playlist Queued",
        description=(
            f"**{name}**\n` {num_tracks} ` tracks\n\nQueued by: {user.mention}"
        ),
        color=BOT_COLOR,
    )

    # Add small alert if the playlist is the max size
    if len(playlist["data"]) == 100:
        embed.description += (
            "\n\n*This playlist is longer than the 100 song"
            " maximum. Only the first 100 songs will be"
            " queued.*"
        )

    return playlist, embed

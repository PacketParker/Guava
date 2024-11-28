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
    Get the album info from the Apple Music API
    """
    album_id = query.split("/album/")[1].split("/")[1]

    try:
        # Get the album info
        response = requests.get(
            f"https://api.music.apple.com/v1/catalog/us/albums/{album_id}",
            headers=headers,
        )

        if response.status_code == 404:
            embed = create_embed(
                title="Album Not Found",
                description=(
                    "The album could not be found as the provided link is"
                    " invalid. Please try again."
                ),
            )
            return None, embed

        if response.status_code == 401:
            LOG.error(
                "Could not authorize with Apple Music API. Likely need to"
                " restart the bot."
            )
            return None, None

        response.raise_for_status()
        # Unpack the album info
        album = response.json()
        name = album["data"][0]["attributes"]["name"]
        artist = album["data"][0]["attributes"]["artistName"]
        num_tracks = len(album["data"][0]["relationships"]["tracks"]["data"])
    except IndexError:
        LOG.error("Failed unpacking Apple Music album info")
        return None, None
    except (JSONDecodeError, requests.HTTPError):
        LOG.error("Failed making request to Apple Music API")
        return None, None

    # Extract artwork URL, if available
    artwork_url = (
        album["data"][0]["attributes"].get("artwork", {}).get("url", None)
    )
    if artwork_url:
        artwork_url = artwork_url.replace("{w}x{h}", "300x300")

    embed = create_embed(
        title="Album Queued",
        description=(
            f"**{name}** by **{artist}**\n"
            f"` {num_tracks} ` tracks\n\n"
            f"Queued by: {user.mention}"
        ),
        thumbnail=artwork_url,
    )

    return album, embed

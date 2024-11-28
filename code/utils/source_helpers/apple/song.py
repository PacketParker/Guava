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
    Get the song info from the Apple Music API
    """
    song_id = query.split("/album/")[1].split("?i=")[1]

    try:
        # Get the song info
        response = requests.get(
            f"https://api.music.apple.com/v1/catalog/us/songs/{song_id}",
            headers=headers,
        )

        if response.status_code == 404:
            embed = create_embed(
                title="Song Not Found",
                description=(
                    "The song could not be found as the provided link is"
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
        # Unpack the song info
        song = response.json()
        name = song["data"][0]["attributes"]["name"]
        artist = song["data"][0]["attributes"]["artistName"]
    except IndexError:
        LOG.error("Failed unpacking Apple Music song info")
        return None, None
    except (JSONDecodeError, requests.HTTPError):
        LOG.error("Failed making request to Apple Music API")
        return None, None

    # Extract artwork URL, if available
    artwork_url = (
        song["data"][0]["attributes"].get("artwork", {}).get("url", None)
    )
    if artwork_url:
        artwork_url = artwork_url.replace("{w}x{h}", "300x300")

    embed = create_embed(
        title="Song Queued",
        description=f"**{name}** by **{artist}**\n\nQueued by {user.mention}",
        thumbnail=artwork_url,
    )

    return song, embed

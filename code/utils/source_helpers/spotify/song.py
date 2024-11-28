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
    Get the song info from the Spotify API
    """
    song_id = query.split("/track/")[1]

    try:
        # Get the song info
        response = requests.get(
            f"https://api.spotify.com/v1/tracks/{song_id}",
            headers=headers,
        )

        if response.status_code == 404:
            embed = discord.Embed(
                title="Song Not Found",
                description=(
                    "The song could not be found as the provided link is"
                    " invalid. Please try again."
                ),
                color=BOT_COLOR,
            )
            return None, embed

        if response.status_code == 401:
            LOG.error(
                "Could not authorize with Spotify API. Likely need to"
                " restart the bot."
            )
            return None, None

        response.raise_for_status()
        # Unpack the song info
        song = response.json()
        name = song["name"]
        artist = song["artists"][0]["name"]
        artwork_url = song["album"]["images"][0]["url"]
    except IndexError:
        LOG.error("Failed unpacking Spotify song info")
        return None, None
    except (JSONDecodeError, requests.HTTPError):
        LOG.error("Failed making request to Spotify API")
        return None, None

    embed = discord.Embed(
        title="Song Queued",
        description=f"**{name}** by **{artist}**\n\nQueued by {user.mention}",
        color=BOT_COLOR,
    )
    embed.set_thumbnail(url=artwork_url)
    embed.set_footer(
        text=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + " UTC"
    )

    return song, embed

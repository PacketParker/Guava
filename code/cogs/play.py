import discord
import datetime
from discord import app_commands
from discord.ext import commands
from cogs.music import Music
from lavalink import LoadType
import re
from cogs.music import LavalinkVoiceClient

from global_variables import BOT_COLOR


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
            return await interaction.response.send_message(embed=embed)

        if "music.apple.com" in query:
            embed = discord.Embed(
                title="Apple Music Not Supported",
                description="Unfortunately, Apple Music does not allow bots to stream from their platform. Try sending a link for a different platform, or simply type the name of the song and I will automatically find it on a supported platform.",
                color=BOT_COLOR,
            )
            return await interaction.response.send_message(embed=embed)

        if not url_rx.match(query):
            ytsearch = f"scsearch:{query}"
            results = await player.node.get_tracks(ytsearch)

            if not results.tracks or results.load_type in (
                LoadType.EMPTY,
                LoadType.ERROR,
            ):
                scsearch = f"dzsearch:{query}"
                results = await player.node.get_tracks(scsearch)
        else:
            results = await player.node.get_tracks(query)

        embed = discord.Embed(color=BOT_COLOR)

        if not results.tracks or results.load_type in (LoadType.EMPTY, LoadType.ERROR):
            embed.title = "Nothing Found"
            embed.description = "Nothing for that query could be found. If this continues happening for other songs, please run `/bug` to let the developer know."
            return await interaction.response.send_message(embed=embed, ephemeral=True)

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

            embed.title = "Track Queued"
            embed.description = f"**{track.title}** by **{track.author}**\n\nQueued by: {interaction.user.mention}"
            embed.set_thumbnail(url=track.artwork_url)
            embed.set_footer(
                text=datetime.datetime.now(datetime.timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                + " UTC"
            )

            player.add(requester=interaction.user, track=track)
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

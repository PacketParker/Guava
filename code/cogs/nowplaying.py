import discord
import datetime
from discord import app_commands
from discord.ext import commands
from cogs.music import Music
import lavalink

from global_variables import BOT_COLOR


class NowPlaying(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command()
    @app_commands.check(Music.create_player)
    async def np(self, interaction: discord.Interaction):
        "Show what song is currently playing"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        time_in = str(datetime.timedelta(milliseconds=player.position))[:-7]
        total_duration = lavalink.utils.format_time(player.current.duration)
        # If total_duration has no hours, then remove the hour part from both times
        if total_duration.split(":")[0] == "00":
            time_in = time_in[2:]
            total_duration = total_duration[3:]

        embed = discord.Embed(
            title="Now Playing 🎶",
            description=f"**[{player.current.title}]({player.current.uri})** by {player.current.author}\n{f'` {time_in}/{total_duration} `'}\n\nQueued by: {player.current.requester.mention}",
            color=BOT_COLOR,
        )
        embed.set_thumbnail(url=player.current.artwork_url)
        embed.set_footer(
            text=datetime.datetime.now(datetime.timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            + " UTC"
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(NowPlaying(bot))

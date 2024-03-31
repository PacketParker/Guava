import discord
import datetime
from discord import app_commands
from discord.ext import commands
from cogs.music import Music
import math
import lavalink

from global_variables import BOT_COLOR


class Queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command()
    @app_commands.check(Music.create_player)
    @app_commands.describe(page="Queue page number - leave blank if you are unsure")
    async def queue(self, interaction: discord.Interaction, page: int = 1):
        "See the current queue of songs"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        if not player.queue:
            embed = discord.Embed(
                title="Nothing Queued",
                description="Nothing is currently in the queue, add a song with the `/play` command.",
                color=BOT_COLOR,
            )
            embed.set_footer(
                text=datetime.datetime.now(datetime.timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                + " UTC"
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue_list = ""
        for index, track in enumerate(player.queue[start:end], start=start):
            # Change ms duration to hour, min, sec in the format of 00:00:00
            track_duration = lavalink.utils.format_time(track.duration)
            # If the track is less than an hour, remove the hour from the duration
            if track_duration.split(":")[0] == "00":
                track_duration = track_duration[3:]

            queue_list += f"`{index+1}. ` [{track.title}]({track.uri}) - {track.author} `({track_duration})`\n"

        embed = discord.Embed(
            title=f"Queue for {interaction.guild.name}",
            description=f"**{len(player.queue)} tracks total**\n\n{queue_list}",
            color=BOT_COLOR,
        )
        embed.set_footer(text=f"Viewing page {page}/{pages}")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Queue(bot))

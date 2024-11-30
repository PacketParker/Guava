import discord
import datetime
from discord import app_commands
from discord.ext import commands
from cogs.music import Music
import math
import lavalink

from utils.config import create_embed

"""
Create an embed for the queue given the current queue and desired page number/pages
"""


def create_queue_embed(queue: list, page: int, pages: int):
    items_per_page = 10
    start = (page - 1) * items_per_page
    end = start + items_per_page

    queue_list = ""
    for index, track in enumerate(queue[start:end], start=start):
        # Change ms duration to hour, min, sec in the format of 00:00:00
        track_duration = lavalink.utils.format_time(track.duration)
        # If the track is less than an hour, remove the hour from the duration
        if track_duration.split(":")[0] == "00":
            track_duration = track_duration[3:]

        queue_list += (
            f"`{index+1}. ` [{track.title}]({track.uri}) -"
            f" {track.author} `({track_duration})`\n"
        )

    embed = create_embed(
        title=f"Current Song Queue",
        description=f"**{len(queue)} total tracks**\n\n{queue_list}",
        footer=f"Page {page}/{pages}",
    )
    return embed


class Queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.check(Music.create_player)
    @app_commands.describe(
        page="Queue page number - leave blank if you are unsure"
    )
    async def queue(self, interaction: discord.Interaction, page: int = 1):
        "See the current queue of songs"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        pages = math.ceil(len(player.queue) / 10)
        # Force page to 1 if an invalid page is provided
        if page < 1 or page > pages:
            page = 1

        if not player.queue:
            embed = create_embed(
                title="Nothing Queued",
                description=(
                    "Nothing is currently in the queue, add a song with the"
                    " </play:1224840890368000172> command."
                ),
            )
            return await interaction.response.send_message(
                embed=embed, ephemeral=True
            )

        embed = create_queue_embed(player.queue, page, pages)
        view = QueueView(page, pages, player.queue)
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Queue(bot))


class QueueView(discord.ui.View):
    def __init__(self, page: int, pages: int, queue: list):
        super().__init__()
        self.page = page
        self.pages = pages
        self.queue = queue
        # Create the previous and next buttons
        self.previous_button = discord.ui.Button(
            label="Previous", style=discord.ButtonStyle.gray
        )
        # Determine if the button should be disabled, add callback, add to view
        self.previous_button.disabled = self.page <= 1
        self.previous_button.callback = self.previous_page
        self.add_item(self.previous_button)

        self.next_button = discord.ui.Button(
            label="Next", style=discord.ButtonStyle.gray
        )
        self.next_button.disabled = self.page >= self.pages
        self.next_button.callback = self.next_page
        self.add_item(self.next_button)

    async def previous_page(self, interaction: discord.Interaction):
        # Decrement the page number, recreate the embed, determine if the
        # button should be disabled, and update the message
        self.page -= 1
        embed = create_queue_embed(self.queue, self.page, self.pages)
        self.previous_button.disabled = self.page <= 1
        self.next_button.disabled = self.page >= self.pages
        await interaction.response.edit_message(embed=embed, view=self)

    async def next_page(self, interaction: discord.Interaction):
        # Increment the page number, recreate the embed, determine if the
        # button should be disabled, and update the message
        self.page += 1
        embed = create_queue_embed(self.queue, self.page, self.pages)
        self.previous_button.disabled = self.page <= 1
        self.next_button.disabled = self.page >= self.pages
        await interaction.response.edit_message(embed=embed, view=self)

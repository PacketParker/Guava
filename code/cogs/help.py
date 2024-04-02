import discord
from discord.ext import commands
import re
from discord import app_commands

from global_variables import BOT_COLOR, BOT_INVITE_LINK


class InviteButton(discord.ui.View):
    def __init__(self, timeout=180.0):
        super().__init__(timeout=timeout)
        self.value = None
        self.add_item(discord.ui.Button(label="Invite Me", url=BOT_INVITE_LINK, row=1))


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def help(self, interaction: discord.Interaction):
        "Sends the bots commands"

        embed = discord.Embed(
            title=f":musical_note: Guava Help :musical_note:", color=BOT_COLOR
        )
        embed.add_field(
            name="`/play <name/URL>`", value="Plays the requested song", inline=False
        )
        embed.add_field(
            name="`/skip`",
            value="Skips the song that is currently playing",
            inline=False,
        )
        embed.add_field(
            name="`/queue (page #)`",
            value="Sends the songs currently in queue",
            inline=False,
        )
        embed.add_field(
            name="`/stop`",
            value="Stops music, clears queue, and leaves VC",
            inline=False,
        )
        embed.add_field(
            name="`/np`", value="Sends the song that is currently playing", inline=False
        )
        embed.add_field(
            name="`/clear`", value="Completely clears the queue", inline=False
        )
        embed.add_field(
            name="`/remove <song #>`",
            value="Removes the specified song from the queue",
            inline=False,
        )
        embed.add_field(
            name="`/repeat <song/queue/off>`",
            value="Forever repeats the current song, queue, or turns repetition off",
            inline=False,
        )
        embed.add_field(
            name="`/shuffle <on/off>`",
            value="Turns song shuffling on or off",
            inline=False,
        )
        embed.add_field(
            name="`/pause`", value="Pauses the currently playing song", inline=False
        )
        embed.add_field(name="`/resume`", value="Resumes the paused song", inline=False)

        embed.add_field(
            name="`/bug`",
            value="Fill out a bug report to let the developer know of any issues",
            inline=False,
        )
        embed.add_field(
            name="`/feedback`",
            value="Give the developer feedback about Guava",
            inline=False,
        )

        embed.set_thumbnail(url=self.bot.user.avatar.url)

        view = InviteButton()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Help(bot))

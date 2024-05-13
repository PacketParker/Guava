import discord
import datetime
from discord import app_commands
from discord.ext import commands
from cogs.music import Music
import asyncio

from global_variables import BOT_COLOR
from custom_source import LoadError


class Skip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.check(Music.create_player)
    @app_commands.describe(number="Optional: Number of songs to skip, default is 1")
    async def skip(self, interaction: discord.Interaction, number: int = 1):
        "Skips the song that is currently playing"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        embed = discord.Embed(color=BOT_COLOR)

        if number != 1:
            if number < 1:
                embed.title = "Invalid Number"
                embed.description = "The number option cannot be less than 1"
                return await interaction.response.send_message(
                    embed=embed, ephemeral=True
                )

            elif number > len(player.queue):
                embed.title = "Number too Large"
                embed.description = "The number you entered is larger than the number of songs in queue. If you want to stop playing music entirely, try the `/stop` command."
                return await interaction.response.send_message(
                    embed=embed, ephemeral=True
                )
            else:
                for i in range(number - 2, -1, -1):
                    player.queue.pop(i)

        # If there is a next song, get it
        try:
            next_song = player.queue[0]
        except IndexError:
            pass

        # Sometimes when a playlist/album of custom source tracks are loaded, one is not able to be found
        # so, when a user attempts to skip to that track, we get a LoadError. In this case, just pass it.
        try:
            await player.skip()
        except LoadError:
            pass
            await player.skip()

        if not player.current:
            embed = discord.Embed(
                title="End of Queue",
                description=f"All songs in queue have been played. Thank you for using Guava :wave:\n\nIssued by: {interaction.user.mention}",
                color=BOT_COLOR,
            )
            return await interaction.response.send_message(embed=embed)

        # It takes a sec for the new track to be grabbed and played
        # So just wait a sec before sending the message
        await asyncio.sleep(0.5)
        embed = discord.Embed(
            title="Track Skipped",
            description=f"**Now Playing: [{next_song.title}]({next_song.uri})** by {next_song.author}\n\nQueued by: {next_song.requester.mention}",
            color=BOT_COLOR,
        )
        embed.set_thumbnail(url=next_song.artwork_url)
        embed.set_footer(
            text=datetime.datetime.now(datetime.timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            + " UTC"
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Skip(bot))

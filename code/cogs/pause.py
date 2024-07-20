import discord
import datetime
from discord import app_commands
from discord.ext import commands
from cogs.music import Music

from utils.config import BOT_COLOR


class Pause(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.check(Music.create_player)
    async def pause(self, interaction: discord.Interaction):
        "Pauses the song that is currently playing"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        await player.set_pause(pause=True)
        embed = discord.Embed(
            title=f"Music Now Paused ⏸️",
            description=f"**[{player.current.title}]({player.current.uri})**\n\nQueued by: {player.current.requester.mention}",
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
    await bot.add_cog(Pause(bot))

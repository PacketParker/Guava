import discord
import datetime
from discord import app_commands
from discord.ext import commands
from cogs.music import Music

from utils.config import BOT_COLOR


class Stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.check(Music.create_player)
    async def stop(self, interaction: discord.Interaction):
        "Disconnects the bot from the voice channel and clears the queue"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        try:
            self.bot.autoplay.remove(interaction.guild.id)
        except ValueError:
            pass
        player.queue.clear()
        await player.stop()
        await interaction.guild.voice_client.disconnect(force=True)

        embed = discord.Embed(
            title="Queue Cleared and Music Stopped",
            description=f"Thank you for using me :wave:\n\nIssued by: {interaction.user.mention}",
            color=BOT_COLOR,
        )
        embed.set_footer(
            text=datetime.datetime.now(datetime.timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            + " UTC"
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Stop(bot))

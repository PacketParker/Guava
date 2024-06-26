import discord
import datetime
from discord import app_commands
from discord.ext import commands
from cogs.music import Music

from config import BOT_COLOR


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.check(Music.create_player)
    async def clear(self, interaction: discord.Interaction):
        "Clear the entire queue of songs"
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        player.queue.clear()
        embed = discord.Embed(
            title="Queue Cleared",
            description=f"The queue has been cleared of all songs!\n\nIssued by: {interaction.user.mention}",
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
    await bot.add_cog(Clear(bot))

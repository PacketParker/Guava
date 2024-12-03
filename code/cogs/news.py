import discord
from discord import app_commands
from discord.ext import commands

from utils.config import BOT_COLOR


class News(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def news(self, interaction: discord.Interaction):
        "Get recent news and updates about the bot"
        embed = discord.Embed(
            title="Recent News and Updates",
            description=(
                "View recent code commits"
                " [here](https://github.com/packetparker/guava/commits)\n\u200b"
            ),
            color=BOT_COLOR,
        )

        embed.add_field(
            name="**Limited YouTube Support**",
            value=(
                "Support for YouTube links and searches has been added. This"
                " is currently in a testing phase and is not guaranteed to"
                " work. If you encounter any issues, please submit a but"
                " report."
            ),
            inline=False,
        )

        embed.add_field(
            name="**General Improvements**",
            value=(
                "Quality of life updates and general improvements have been"
                " made. Hopefully there are no new bugs, but please report any"
                " with </bug:1224840889906499626>."
            ),
            inline=False,
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(News(bot))

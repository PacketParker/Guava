import discord
from discord import app_commands
from discord.ext import commands

from config import BOT_COLOR


class News(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def news(self, interaction: discord.Interaction):
        "Get recent news and updates about the bot"
        embed = discord.Embed(
            title="Updated News (July 11, 2024) :newspaper2:",
            description="View recent code commits [here](https://github.com/packetparker/guava/commits)\n\u200b",
            color=BOT_COLOR,
        )

        embed.add_field(
            name="**Autoplay Update**",
            value="> Autoplay is now much more stable after a revamp of the previous system. If you experienced short outages recently, this was due to the update. Thank you for your patience!",
            inline=False,
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(News(bot))
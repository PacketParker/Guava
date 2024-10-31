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
            title="Recent News :newspaper2:",
            description=(
                "View recent code commits"
                " [here](https://github.com/packetparker/guava/commits)\n\u200b"
            ),
            color=BOT_COLOR,
        )

        embed.add_field(
            name="**Lyrics!**",
            value=(
                "> You can now get lyrics for the song that is currently"
                " playing. Just use the `/lyrics` command! Some songs may not"
                " have lyrics available, but the bot will do its best to find"
                " them."
            ),
        )

        embed.add_field(
            name="**Apple Music Support!**",
            value=(
                "> After some trial and error, you can now play music through"
                " Apple Music links. Just paste the link and the bot will do"
                " the rest!"
            ),
        )

        embed.add_field(
            name="**Autoplay Update**",
            value=(
                "> Autoplay is now much more stable after a revamp of the"
                " previous system. If you experienced short outages recently,"
                " this was due to the update. Thank you for your patience!"
            ),
            inline=False,
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(News(bot))

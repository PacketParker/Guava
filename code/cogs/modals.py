import discord
from discord import app_commands
from discord.ext import commands

from feedback import FeedbackForm


class Modals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def feedback(self, interaction: discord.Interaction):
        "Send bot feeback to the developer"
        await interaction.response.send_modal(FeedbackForm(self.bot))


async def setup(bot):
    await bot.add_cog(Modals(bot))

import discord
from discord import app_commands
from discord.ext import commands

from utils.config import BOT_COLOR, FEEDBACK_CHANNEL_ID


class FeedbackForm(discord.ui.Modal, title="Give feedback about the bot"):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    name = discord.ui.TextInput(
        label="Discord username",
        placeholder="EX: itsmefreddy01...",
    )
    positive = discord.ui.TextInput(
        label="What do you like about the bot?",
        style=discord.TextStyle.long,
        placeholder="Your response here...",
        required=True,
        max_length=500,
    )
    negative = discord.ui.TextInput(
        label="What should be changed about the bot?",
        style=discord.TextStyle.long,
        placeholder="Your response here...",
        required=True,
        max_length=500,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Thank you for your feedback. We love hearing from users!", ephemeral=True
        )
        channel = self.bot.get_channel(FEEDBACK_CHANNEL_ID)

        embed = discord.Embed(
            title="Bot Feedback",
            description=f"Submitted by {self.name} (<@{interaction.user.id}>)",
            color=BOT_COLOR,
        )
        embed.add_field(name="Positive:", value=f"{self.positive}", inline=False)
        embed.add_field(name="Negative:", value=f"{self.negative}", inline=False)

        await channel.send(embed=embed)


class Feedback(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def feedback(self, interaction: discord.Interaction):
        "Send bot feeback to the developer"
        await interaction.response.send_modal(FeedbackForm(self.bot))


async def setup(bot):
    await bot.add_cog(Feedback(bot))

import discord
from discord import app_commands
from discord.ext import commands

from global_variables import BOT_COLOR, BUG_CHANNEL_ID, FEEDBACK_CHANNEL_ID


class BugReport(discord.ui.Modal, title="Report a bug"):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    name = discord.ui.TextInput(
        label="Discord username",
        placeholder="EX: itsmefreddy01...",
    )
    command = discord.ui.TextInput(
        label="Command with error", placeholder="EX: skip...", required=True
    )
    report = discord.ui.TextInput(
        label="A detailed report of the bug",
        style=discord.TextStyle.long,
        placeholder="Type your report here...",
        required=True,
        max_length=500,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Thanks for your bug report. We will get back to you as soon as possible",
            ephemeral=True,
        )
        channel = self.bot.get_channel(BUG_CHANNEL_ID)

        embed = discord.Embed(
            title="Bug Report",
            description=f"Submitted by {self.name} (<@{interaction.user.id}>)",
            color=BOT_COLOR,
        )
        embed.add_field(
            name="Command with issue:", value=f"{self.command}", inline=False
        )
        embed.add_field(name="Report:", value=f"{self.report}", inline=False)

        await channel.send(embed=embed)


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


class Modals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def bug(self, interaction: discord.Interaction):
        "Send a bug report to the developer"
        await interaction.response.send_modal(BugReport(self.bot))

    @app_commands.command()
    async def feedback(self, interaction: discord.Interaction):
        "Send bot feeback to the developer"
        await interaction.response.send_modal(FeedbackForm(self.bot))


async def setup(bot):
    await bot.add_cog(Modals(bot))

import discord

from global_variables import BUG_CHANNEL_ID, BOT_COLOR


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

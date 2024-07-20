import discord
from discord.ext import commands
from discord import app_commands

from utils.config import BOT_COLOR, BOT_INVITE_LINK

commands_and_descriptions = {
    "play": {
        "description": "Plays the requested song",
        "arguments": {"query": "Name or link of the song you want to play"},
        "usage": "/play <query>",
    },
    "skip": {
        "description": "Skips the song that is currently playing",
        "optional_arguments": {
            "number": "The number of songs to skip - leave blank to skip just the current song"
        },
        "usage": "/skip (number)",
    },
    "queue": {
        "description": "Sends the songs currently added to the queue",
        "optional_arguments": {
            "page": "Page number of the queue to view - leave blank to see only the first page"
        },
        "usage": "/queue (page)",
    },
    "stop": {
        "description": "Stops all music, clears the queue, and leave the voice channel",
        "usage": "/stop",
    },
    "np": {"description": "Sends the song that is currently playing", "usage": "/np"},
    "clear": {"description": "Removes all songs from the queue", "usage": "/clear"},
    "remove": {
        "description": "Removes the specified song from the queue",
        "arguments": {
            "number": "The queue number of the song that should be removed from the queue"
        },
        "usage": "/remove <number>",
    },
    "autoplay": {
        "description": "Keep the music playing forever with music suggestions from OpenAI",
        "arguments": {
            "on": "Turn autoplay feature on",
            "off": "Turn autoplay feature off",
        },
        "usage": "/autoplay <on/off>",
    },
    "repeat": {
        "description": "Changes the looping state of the bot",
        "arguments": {
            "song": "Repeats the song that is currently playing until changed",
            "queue": "Continuously repeat the songs in the queue until turned off",
            "off": "Stop all song or queue repetition",
        },
        "usage": "/repeat <song/queue/off>",
    },
    "shuffle": {
        "description": "Turn song shuffling on or off",
        "arguments": {
            "on": "Turns randomized song shuffling on",
            "off": "Turns shuffling off",
        },
        "usage": "/shuffle <on/off>",
    },
    "pause": {
        "description": "Pause the song that is currently playing",
        "usage": "/pause",
    },
    "resume": {
        "description": "Resume the song that is currently paused",
        "usage": "/resume",
    },
    "news": {
        "description": "Get recent news and updates about the bot",
        "usage": "/news",
    },
    "bug": {
        "description": "Fill out a bug report form to alert the developer of issues",
        "usage": "/bug",
    },
    "feedback": {
        "description": "Fill out a form to give the developer feedback on the bot",
        "usage": "/feedback",
    },
}


class HelpView(discord.ui.View):
    def __init__(self, timeout=180.0):
        super().__init__(timeout=timeout)
        self.add_item(discord.ui.Button(label="Invite Me", url=BOT_INVITE_LINK, row=1))

    @discord.ui.button(
        label="View All Commands", style=discord.ButtonStyle.green, row=1
    )
    async def view_all_commands(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        embed = discord.Embed(
            title=":musical_note:  All Commands  :musical_note:",
            description="**Check out recent news and updates about the bot with the </news:1260842465666007040> command!\n\u200b**",
            color=BOT_COLOR,
        )

        embed.add_field(
            name="All Commands",
            value=", ".join(
                [f"`{command}`" for command in commands_and_descriptions.keys()]
            ),
        )

        await interaction.response.edit_message(embed=embed, view=None)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.describe(command="Name of the command you want more information on")
    async def help(self, interaction: discord.Interaction, command: str = None):
        "Sends the bots commands"

        if command == None:
            embed = discord.Embed(
                title=f":musical_note:  Help  :musical_note:",
                description="**Check out recent news and updates about the bot with the </news:1260842465666007040> command!\n\u200b**",
                color=BOT_COLOR,
            )

            embed.add_field(
                name="**Use Me**",
                value="> To get started, use the </play:1224840890368000172> command and enter the name or link to the song of your choice.",
                inline=False,
            )
            embed.add_field(
                name="**Full Command List**",
                value='> To view of a list of all available commands, click the "View All Commands" button below.',
                inline=False,
            )
            embed.add_field(
                name="**Help for Specific Commands**",
                value="> If you want more information on how to use a specific command, use the </help:1224854217597124610> command and include the specific command.",
                inline=False,
            )

            embed.set_thumbnail(url=self.bot.user.avatar.url)

            view = HelpView()
            await interaction.response.send_message(
                embed=embed, view=view, ephemeral=True
            )

        elif command in commands_and_descriptions.keys():
            command = command.lower().strip()
            embed = discord.Embed(
                title=f"**{command}**",
                description=f"{commands_and_descriptions[command]['description']}",
                color=BOT_COLOR,
            )

            try:
                if commands_and_descriptions[command]["arguments"]:
                    arguments_value = ""
                    for argument, explanation in commands_and_descriptions[command][
                        "arguments"
                    ].items():
                        arguments_value += f"{argument}\n> {explanation}\n\n"

                    embed.add_field(
                        name="Arguments", value=arguments_value, inline=False
                    )
            except KeyError:
                pass

            try:
                if commands_and_descriptions[command]["optional_arguments"]:
                    arguments_value = ""
                    for argument, explanation in commands_and_descriptions[command][
                        "optional_arguments"
                    ].items():
                        arguments_value += f"{argument}\n> {explanation}\n\n"

                    embed.add_field(
                        name="Optional Arguments", value=arguments_value, inline=False
                    )
            except KeyError:
                pass

            embed.add_field(
                name="Usage", value=f"` {commands_and_descriptions[command]['usage']} `"
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)

            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            embed = discord.Embed(
                title="Command Doesn't Exist",
                description=f"The command you entered (` {command} `) does not exist, please try again with a different command name.",
                color=BOT_COLOR,
            )

            view = HelpView()
            await interaction.response.send_message(
                embed=embed, view=view, ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(Help(bot))

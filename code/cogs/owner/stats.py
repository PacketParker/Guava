from discord.ext import commands, tasks
import sqlite3
import discord
import os
import lavalink

from utils.config import BOT_COLOR, LOG


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_load(self):
        if not os.path.exists("data"):
            os.makedirs("data")

        if not os.access("data/count.db", os.W_OK):
            LOG.error("Cannot write to data/count.db - check permissions")
            return

        connection = sqlite3.connect("data/count.db")
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS count (command_name, count, PRIMARY"
            " KEY (command_name))"
        )
        connection.commit()
        connection.close()

        self.dump_count.start()

    @tasks.loop(seconds=30)
    async def dump_count(self):
        connection = sqlite3.connect("data/count.db")
        cursor = connection.cursor()

        for command_name, count in self.bot.temp_command_count.items():
            try:
                cursor.execute(
                    "INSERT INTO count (command_name, count) VALUES (?, ?)",
                    (command_name, count),
                )
            except sqlite3.IntegrityError:
                cursor.execute(
                    "UPDATE count SET count = count + ? WHERE"
                    " command_name = ?",
                    (count, command_name),
                )

        connection.commit()
        connection.close()
        self.bot.temp_command_count = {}

    @commands.Cog.listener()
    async def on_app_command_completion(self, interaction, command):
        try:
            self.bot.temp_command_count[interaction.command.name] += 1
        except KeyError:
            self.bot.temp_command_count[interaction.command.name] = 1

    @commands.command()
    @commands.dm_only()
    @commands.is_owner()
    async def stats(self, ctx: commands.Context):
        connection = sqlite3.connect("data/count.db")
        cursor = connection.cursor()

        # Pull the top 5 commands being run
        data = cursor.execute(
            "SELECT * FROM count ORDER BY count DESC LIMIT 5"
        ).fetchall()

        # Get the combined total amount of commands run
        total_commands = cursor.execute(
            "SELECT SUM(count) FROM count"
        ).fetchone()[0]

        embed = discord.Embed(
            title="Statistics",
            description=(
                f"Total Guilds: `{len(self.bot.guilds):,}`\n"
                f"Total Commands: `{total_commands:,}`\n\n"
            ),
            color=BOT_COLOR,
        )

        # Determine the content of the Lavalink description
        if self.bot.lavalink:
            embed.description += (
                "Total Players:"
                f" `{len(self.bot.lavalink.get_players())}`\n"
                "Load:"
                f" `{round(self.bot.lavalink.nodes[0].stats.lavalink_load * 100, 2)}%`"
            )
        else:
            embed.description += (
                "Total Players: `NO LAVALINK CONNECTION`\n"
                "Load: `NO LAVALINK CONNECTION`"
            )

        for entry in data:
            embed.add_field(
                name=entry[0], value=f"` {entry[1]:,} `", inline=True
            )

        connection.close()
        await ctx.send(embed=embed)

    @stats.error
    async def stats_error(self, ctx, error):
        return


async def setup(bot):
    await bot.add_cog(Stats(bot))

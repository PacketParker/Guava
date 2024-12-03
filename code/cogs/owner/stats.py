from discord.ext import commands, tasks
import sqlite3
import discord
import os

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

    def millis_to_readable(self, ms):
        hours = ms // 3600000
        ms %= 3600000
        minutes = ms // 60000
        ms %= 60000
        seconds = ms // 1000
        milliseconds = ms % 1000

        return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

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

    @commands.group(invoke_without_command=True)
    @commands.dm_only()
    @commands.is_owner()
    async def stats(self, ctx: commands.Context):
        await ctx.author.send(
            f"This is a group command. Use `{self.bot.command_prefix}stats"
            " bot/lavalink` to get specific statistics."
        )

    @stats.command()
    @commands.dm_only()
    @commands.is_owner()
    async def bot(self, ctx: commands.Context):
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

        for entry in data:
            embed.add_field(
                name=entry[0], value=f"` {entry[1]:,} `", inline=True
            )

        connection.close()
        await ctx.send(embed=embed)

    @bot.error
    async def bot_error(self, ctx, error):
        return

    @stats.command()
    @commands.dm_only()
    @commands.is_owner()
    async def lavalink(self, ctx: commands.Context):
        if not self.bot.lavalink:
            return await ctx.send("No connection with Lavalink.")

        embed = discord.Embed(
            title="Lavalink Statistics",
            color=BOT_COLOR,
        )

        for node in self.bot.lavalink.nodes:
            embed.add_field(
                name=node.name,
                value=(
                    f"\tPlayers: `{node.stats.players}`\n\tUptime:"
                    f" `{self.millis_to_readable(node.stats.uptime)}`\n\tMemory"
                    f" Used: `{node.stats.memory_used / 1024 / 1024:.2f}MB`\n"
                ),
                inline=True,
            )

        await ctx.send(embed=embed)

    @lavalink.error
    async def lavalink_error(self, ctx, error):
        return


async def setup(bot):
    await bot.add_cog(Stats(bot))

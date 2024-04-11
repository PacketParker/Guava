from discord.ext import commands, tasks
from discord import app_commands
import sqlite3
import discord

from global_variables import BOT_COLOR


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_load(self):
        connection = sqlite3.connect("count.db")
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS count (command_name, count, PRIMARY KEY (command_name))"
        )
        connection.commit()
        connection.close()

        self.dump_count.start()

    @tasks.loop(seconds=30)
    async def dump_count(self):
        connection = sqlite3.connect("count.db")
        cursor = connection.cursor()

        for command_name, count in self.bot.temp_command_count.items():
            try:
                cursor.execute(
                    "INSERT INTO count (command_name, count) VALUES (?, ?)",
                    (command_name, count),
                )
            except sqlite3.IntegrityError:
                cursor.execute(
                    "UPDATE count SET count = count + ? WHERE command_name = ?",
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
        connection = sqlite3.connect("count.db")
        cursor = connection.cursor()

        embed = discord.Embed(title="Command Statistics", color=BOT_COLOR)

        total = 0
        data = cursor.execute("SELECT * FROM count").fetchall()
        for entry in data:
            embed.add_field(name=entry[0], value=f"` {entry[1]} `", inline=True)
            total += entry[1]

        embed.add_field(name="TOTAL", value=f"` {total} `", inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Stats(bot))

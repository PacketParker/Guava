import discord
from discord.ext import commands
import os

from validate_config import create_config
from global_variables import LOG, BOT_TOKEN


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="***",
            activity=discord.Game(name="music!"),
            intents=discord.Intents.default(),
        )

    async def setup_hook(self):
        create_config()
        for ext in os.listdir("./code/cogs"):
            if ext.endswith(".py"):
                await self.load_extension(f"cogs.{ext[:-3]}")


bot = MyBot()
bot.count_hold = 0
bot.remove_command("help")


@bot.event
async def on_ready():
    LOG.info(f"{bot.user} has connected to Discord.")


if __name__ == "__main__":
    bot.run(BOT_TOKEN)

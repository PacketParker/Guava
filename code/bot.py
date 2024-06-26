import discord
from discord.ext import commands, tasks
import os
import requests

import config


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="***",
            activity=discord.Game(name="music!"),
            intents=discord.Intents.default(),
        )

    async def setup_hook(self):
        get_access_token.start()
        for ext in os.listdir("./code/cogs"):
            if ext.endswith(".py"):
                await self.load_extension(f"cogs.{ext[:-3]}")
        for ext in os.listdir("./code/cogs/owner"):
            if ext.endswith(".py"):
                await self.load_extension(f"cogs.owner.{ext[:-3]}")


bot = MyBot()
bot.remove_command("help")
bot.temp_command_count = {}  # command_name: count
bot.autoplay = []  # guild_id, guild_id, etc.


@bot.event
async def on_ready():
    config.LOG.info(f"{bot.user} has connected to Discord.")


@tasks.loop(minutes=45)
async def get_access_token():
    auth_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": config.SPOTIFY_CLIENT_ID,
        "client_secret": config.SPOTIFY_CLIENT_SECRET,
    }
    response = requests.post(auth_url, data=data)
    access_token = response.json()["access_token"]
    bot.spotify_headers = {"Authorization": f"Bearer {access_token}"}


if __name__ == "__main__":
    config_contents = config.load_config()
    config.validate_config(config_contents)
    bot.run(config.TOKEN)

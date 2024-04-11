import discord
from discord.ext import commands, tasks
import os
import requests

from validate_config import create_config
from global_variables import LOG, BOT_TOKEN, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="***",
            activity=discord.Game(name="music!"),
            intents=discord.Intents.default(),
        )

    async def setup_hook(self):
        create_config()
        get_access_token.start()
        for ext in os.listdir("./code/cogs"):
            if ext.endswith(".py"):
                await self.load_extension(f"cogs.{ext[:-3]}")
        for ext in os.listdir("./code/cogs/owner"):
            if ext.endswith(".py"):
                await self.load_extension(f"cogs.owner.{ext[:-3]}")


bot = MyBot()
bot.remove_command("help")
bot.temp_command_count = {} # command_name: count


@bot.event
async def on_ready():
    LOG.info(f"{bot.user} has connected to Discord.")


@tasks.loop(minutes=45)
async def get_access_token():
    auth_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }
    response = requests.post(auth_url, data=data)
    access_token = response.json()["access_token"]
    bot.spotify_headers = {"Authorization": f"Bearer {access_token}"}


if __name__ == "__main__":
    bot.run(BOT_TOKEN)

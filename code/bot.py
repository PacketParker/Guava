import discord
from discord.ext import commands, tasks
import os
import requests
import openai

import config
from tree import Tree


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="***",
            activity=discord.Game(name="music!"),
            intents=discord.Intents.default(),
            tree_cls=Tree,
        )

    async def setup_hook(self):
        get_access_token.start()
        config.LOG.info("Loading cogs...")
        for ext in os.listdir("./code/cogs"):
            if ext.endswith(".py"):
                if ext[:-3] == "feedback" and config.FEEDBACK_CHANNEL_ID == None:
                    config.LOG.info("Skipped loading feedback cog - channel ID not provided")
                    continue
                if ext[:-3] == "bug" and config.BUG_CHANNEL_ID == None:
                    config.LOG.info("Skipped loading bug cog - channel ID not provided")
                    continue
                await self.load_extension(f"cogs.{ext[:-3]}")
        for ext in os.listdir("./code/cogs/owner"):
            if ext.endswith(".py"):
                await self.load_extension(f"cogs.owner.{ext[:-3]}")

        bot.openai = openai.OpenAI(api_key=config.OPENAI_API_KEY)

    async def on_ready(self):
        config.LOG.info(f"{bot.user} has connected to Discord.")
        config.LOG.info("Startup complete. Sync slash commands by DMing the bot ***sync")


bot = MyBot()
bot.remove_command("help")
bot.temp_command_count = {}  # command_name: count
bot.autoplay = []  # guild_id, guild_id, etc.


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
    config.load_config()
    bot.run(config.TOKEN)

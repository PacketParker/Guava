from discord.ext import commands
import requests

from utils.config import LAVALINK_HOST, LAVALINK_PORT, LAVALINK_PASSWORD, LOG


class POToken(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.dm_only()
    @commands.is_owner()
    async def potoken(self, ctx, token: str = None, visitor_data: str = None):
        """Update the poToken for lavalink youtube support."""
        if not token or not visitor_data:
            return await ctx.send(
                "Missing token and/or visitor data. Format as"
                f" `{self.bot.command_prefix}potoken <token> <visitor"
                " data>`\n\nTo generate a poToken, see"
                " [this](https://github.com/iv-org/youtube-trusted-session-generator)"
            )

        url = f"http://{LAVALINK_HOST}:{LAVALINK_PORT}/youtube"
        request = requests.post(
            url,
            json={"poToken": token, "visitorData": visitor_data},
            headers={"Authorization": LAVALINK_PASSWORD},
        )

        if request.status_code != 204:
            LOG.error("Error updating poToken")
            return await ctx.send(
                "Error setting poToken, YouTube source plugin is likely not"
                " enabled. Read the Guava docs and look"
                " [here](https://github.com/lavalink-devs/youtube-source)."
            )

        LOG.info("poToken successfully updated")
        await ctx.send(
            "Successfully posted the token and visitor data to lavalink."
        )


async def setup(bot):
    await bot.add_cog(POToken(bot))

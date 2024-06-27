import discord
from discord.ext import commands
import lavalink
from lavalink import errors

from config import (
    LAVALINK_HOST,
    LAVALINK_PASSWORD,
    LAVALINK_PORT,
    LOG,
)
from ai_recommendations import add_song_recommendations


class CheckPlayerError(discord.app_commands.AppCommandError):
    def __init__(self, info) -> None:
        self.info = info
        super().__init__()


class LavalinkVoiceClient(discord.VoiceProtocol):
    """
    This is the preferred way to handle external voice sending
    This client will be created via a cls in the connect method of the channel
    see the following documentation:
    https://discordpy.readthedocs.io/en/latest/api.html#voiceprotocol
    """

    def __init__(self, client: commands.Bot, channel: discord.abc.Connectable):
        self.client = client
        self.channel = channel
        self.guild_id = channel.guild.id
        self._destroyed = False

        if not hasattr(self.client, "lavalink"):
            self.client.lavalink = lavalink.Client(client.user.id)
            self.client.lavalink.add_node(
                host=LAVALINK_HOST,
                port=LAVALINK_PORT,
                password=LAVALINK_PASSWORD,
                region="us",
                name="default-node",
            )  # Host, Port, Password, Region
        self.lavalink = self.client.lavalink

    async def on_voice_server_update(self, data):
        lavalink_data = {"t": "VOICE_SERVER_UPDATE", "d": data}
        await self.lavalink.voice_update_handler(lavalink_data)

    async def on_voice_state_update(self, data):
        channel_id = data["channel_id"]

        if not channel_id:
            await self._destroy()
            return

        self.channel = self.client.get_channel(int(channel_id))
        # the data needs to be transformed before being handed down to
        # voice_update_handler
        lavalink_data = {"t": "VOICE_STATE_UPDATE", "d": data}
        await self.lavalink.voice_update_handler(lavalink_data)

    async def connect(
        self,
        *,
        timeout: float,
        reconnect: bool,
        self_deaf: bool = True,
        self_mute: bool = False,
    ) -> None:
        self.lavalink.player_manager.create(guild_id=self.channel.guild.id)
        await self.channel.guild.change_voice_state(
            channel=self.channel, self_mute=self_mute, self_deaf=self_deaf
        )

    async def disconnect(self, *, force: bool) -> None:
        player = self.lavalink.player_manager.get(self.channel.guild.id)
        if not force and not player.is_connected:
            return

        await self.channel.guild.change_voice_state(channel=None)
        player.channel_id = None
        await self._destroy()

    async def _destroy(self):
        self.cleanup()

        if self._destroyed:
            return

        self._destroyed = True

        try:
            await self.lavalink.player_manager.destroy(self.guild_id)
        except lavalink.ClientError:
            pass


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        if not hasattr(
            self.bot, "lavalink"
        ):  # This ensures the client isn't overwritten during cog reloads.
            self.bot.lavalink = lavalink.Client(self.bot.user.id)
            node = self.bot.lavalink.add_node(
                host=LAVALINK_HOST,
                port=LAVALINK_PORT,
                password=LAVALINK_PASSWORD,
                region="us-central",
                connect=False,
            )  # Host, Port, Password, Region, Connect
            try:
                await node.get_version()
            except lavalink.errors.ClientError:
                LOG.error(
                    "Authentication to lavalink node failed. Check your login credentials."
                )
            else:
                await node.connect()
                LOG.info(f"Connected to lavalink node {node.name}")

        self.lavalink: lavalink.Client = self.bot.lavalink
        self.lavalink.add_event_hooks(self)

    def cog_unload(self):
        """Cog unload handler. This removes any event hooks that were registered."""
        self.lavalink._event_hooks.clear()

    async def create_player(interaction: discord.Interaction):
        """Create a player for the guild associated with the interaction, or raise an error"""
        try:
            player = interaction.client.lavalink.player_manager.create(
                interaction.guild.id
            )
        except errors.ClientError:
            raise CheckPlayerError(
                {
                    "title": "Lavalink Error",
                    "description": "An error occured when attempting to use lavalink node. Please submit a bug report if this issue persists.",
                }
            )
        should_connect = interaction.command.name in ("play",)
        voice_client = interaction.guild.voice_client

        if not interaction.user.voice or not interaction.user.voice.channel:
            if voice_client is not None:
                raise CheckPlayerError(
                    {
                        "title": "Not in my VC",
                        "description": "You must join my voice channel to run that command.",
                    }
                )

            raise CheckPlayerError(
                {
                    "title": "No Channel",
                    "description": "You must join a voice channel before you can run that command.",
                }
            )

        if voice_client is None:
            if not should_connect:
                raise CheckPlayerError(
                    {
                        "title": "Not Connected",
                        "description": "I am not connected and playing music right now, therefore that command will not work.",
                    }
                )

            permissions = interaction.user.voice.channel.permissions_for(
                interaction.guild.me
            )

            if not permissions.connect or not permissions.speak:
                raise CheckPlayerError(
                    {
                        "title": "Missing Permissions",
                        "description": "I need the `CONNECT` and `SPEAK` permissions in order to work.",
                    }
                )

            player.store("channel", interaction.channel.id)
        else:
            if int(player.channel_id) != interaction.user.voice.channel.id:
                raise CheckPlayerError(
                    {
                        "title": "Not in my VC",
                        "description": "You must join my voice channel to run that command.",
                    }
                )

        return True

    @lavalink.listener(lavalink.events.QueueEndEvent)
    async def on_queue_end(self, event: lavalink.events.QueueEndEvent):
        guild_id = event.player.guild_id
        guild = self.bot.get_guild(guild_id)
        try:
            self.bot.autoplay.remove(guild_id)
        except ValueError:
            pass

        if guild is not None:
            await guild.voice_client.disconnect(force=True)

    @lavalink.listener(lavalink.events.TrackEndEvent)
    async def on_track_end(self, event: lavalink.events.TrackEndEvent):
        guild_id = event.player.guild_id

        if len(event.player.queue) <= 10 and guild_id in self.bot.autoplay:
            inputs = {}
            for song in event.player.queue[:10]:
                inputs[song.title] = song.author
            await add_song_recommendations(self.bot.user, event.player, 5, inputs)


async def setup(bot):
    await bot.add_cog(Music(bot))

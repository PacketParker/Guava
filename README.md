<h1 align="center">
  <br>
  <img src="guava.png" width="300" alt="Guava Image"></a>
  <br>
  Guava<br>
</h1>

<h3 align="center">
    Dead simple Discord music bot
    <br>
    <a href="https://discord.com/oauth2/authorize?client_id=982806583060885525&permissions=3147776&scope=bot+applications.commands" target="_blank">Invite Guava</a>
</h3>

<p align="center">
  <a href="https://github.com/Rapptz/discord.py/">
     <img src="https://img.shields.io/badge/discord-py-blue.svg" alt="discord.py">
  </a>
  <a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style: Black">
  </a>
  <a href="https://makeapullrequest.com">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg">
  </a>
</p>

# Overview

Guava is a Discord music bot with support for multiple different music and video streaming platforms. Guava is a part of >200 Discord servers and currently supports these services:

- Apple Music
- Spotify
- SoundCloud
- Bandcamp
- Deezer
- Twitch Streams
- Vimeo

Getting started is easy, simply invite Guava to your server and run `/help` to see what all Guava has to offer.

# Want to self-host?
Guava is built on Python and requires a Lavalink node running release `v4` or higher with the [LavaSrc](https://github.com/topi314/LavaSrc) and [youtube-source](https://github.com/lavalink-devs/youtube-source) plugins.

If you would like to run your own version of Guava, continue to read the information below.

*NOTE: No matter which option you choose (Docker or bare metal) you will get a fatal error on first run due to missing the `config.yaml` file. A new config.yaml file will be created for you with the necessary fields for configuration. For information on each configuration field, see [Configuration](#configuration).*

## Docker
To run Guava in Docker, use the provided [docker-compose.yaml](docker-compose.yaml) file as a template for the container.

In addition to the Guava container, you must also create a Lavalink node however you choose (bare metal or docker)

## Bare metal
To run Guava on bare metal, follow the steps below.

1. Install Python 3 and Pip
2. Clone this repository
3. Install the requirements with `pip install -r requirements.txt`
4. Run the `code/bot.py` file
5. Input information into the newly created config.yaml file.
6. Re-run the `code/bot.py` file.

# Configuration

Field | Description | Requirement
--- | --- | ---
TOKEN | The token for your bot. Create a bot at [discord.com/developers](https://discord.com/developers) | **REQUIRED**
BOT_COLOR | `HEX CODE`: Color that will be used for the color of message embeds | **REQUIRED**
BOT_INVITE_LINK | `URL`: Discord Invite link for your bot (shown on the `help` command) | **OPTIONAL** - *Adds an "Invite Me" button to the /help message*
FEEDBACK_CHANNEL_ID | `CHANNEL ID`: Discord channel for feedback messages to be sent to | **OPTIONAL** - *Used for feedback messages*
BUG_CHANNEL_ID | `CHANNEL ID`: Discord channel for bug messages to be sent to | **OPTIONAL** - *Used for bug reporting*
SPOTIFY_CLIENT_ID | `CLIENT ID`: ID from Spotify Developer account | **OPTIONAL** - *Used for Spotify support*
SPOTIFY_CLIENT_SECRET | `CLIENT SECRET`: Secret string from Spotify Developer account | **OPTIONAL** - *Used for Sporify support*
GENIUS_CLIENT_ID | `CLIENT ID`: ID from Genius API Dashboard | **OPTIONAL** - *Used for the /lyrics command*
GENIUS_CLIENT_SECRET | `CLIENT SECRET`: Secret string from Genius API Dashboard | **OPTIONAL** - *Used for the /lyrics command*
OPENAI_API_KEY | API Key from OpenAI for autoplay recommendations | **OPTIONAL** - *Used to support the /autoplay feature*
HOST | Host address for your Lavalink node | **REQUIRED**
PORT | Port for your Lavalink node | **REQUIRED**
PASSWORD | Password to authenticate into the Lavalink node | **REQUIRED**

# Lavalink

For instructions on setting up a Lavalink node on bare metal, look [here](https://lavalink.dev/getting-started/). Refer to the plugin repositories for support on configuring them.

*P.S. Only the Deezer/SoundCloud sources/search providers are needed in the LavaSrc plugin.*

After setting up your Lavalink node, it is highly recommended to configure IPv6 rotation with at least a /64 or /48 block. IPv6 rotation helps to relieve issues from getting rate limited/blocked from YouTube and other sources. There are helpful guides for setting this up which are available on GitHub, however, [this](https://github.com/Nansess/tunnelbroker-guide) is the one that I have used .

An example of my personal `application.yml` configuration file can be found [here](https://github.com/PacketParker/Guava/blob/main/application.yml.example).

<br>

If you have any questions, feel free to email at [contact@pkrm.dev](mailto:contact@pkrm.dev). Thank you for checking out Guava, and happy coding.

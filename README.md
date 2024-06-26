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

- Spotify (Links)
- SoundCloud
- Bandcamp
- Deezer
- Twitch Streams
- Vimeo

Getting started is easy, simply invite Guava to your server and run `/help` to see what all Guava has to offer.

# Want to self-host?
Guava is built on Python and requires a Lavalink node running release `v4` or higher with the LavaSrc plugin. If you would like to configure Guava and run it on your own, follow the steps below.

*NOTE: For information on each configuration variable, look at the [Configuration](#configuration) section of this page.*

*P.S. Some information on starting your own lavalink node can be found [here](#lavalink-information)*

## Docker
To run Guava in Docker, use the provided [docker-compose.yaml](docker-compose.yaml) file as a template for the container.

In addition to the Guava container, you must also create a Lavalink node however you choose (bare metal or docker)

## Bare metal
To run Guava on bare metal, follow the steps below.

*NOTE: On first run you will likely get a critical warning in your console, don't worry, this is expected. It will automatically create a `config.ini` file for you in the root of the directory with all of the necessary configuration options.*

1. Install Python and Pip
2. Clone this repository
3. Install the requirements with `pip install -r requirements.txt`
4. Run the `code/bot.py` file
5. Input information into the newly created config.ini file.
6. Re-run the `code/bot.py` file.

# Configuration

Field | Description | Requirement
--- | --- | ---
TOKEN | The token for your bot. Create a bot at [discord.com/developers](https://discord.com/developers) | **REQUIRED**
BOT_COLOR | `HEX CODE`: Color that will be used for the color of message embeds | **REQUIRED**
BOT_INVITE_LINK | `URL`: Discord Invite link for your bot (shown on the `help` command) | **REQUIRED**
FEEDBACK_CHANNEL_ID | `CHANNEL ID`: Discord channel for feedback messages to be sent to | **OPTIONAL**
BUG_CHANNEL_ID | `CHANNEL ID`: Discord channel for bug messages to be sent to | **OPTIONAL**
SPOTIFY_CLIENT_ID | Client ID from Spotify Developer account | **REQUIRED**
SPOTIFY_CLIENT_SECRET | Client Secret from Spotify Developer account | **REQUIRED**
OPENAI_API_KEY | API Key from OpenAI for autoplay recommendations | **REQUIRED**
HOST | Host address for your Lavalink node | **REQUIRED**
PORT | Port for your Lavalink node | **REQUIRED**
PASSWORD | Password to authenticate into the Lavalink node | **REQUIRED**

# Lavalink Information

As previously state, a Lavalink node running at least `v4` with the LavaSrc plugin is required. Due to the plugin requirement, it is unlikely that you will be able to use a free/public Lavalink node.

For instructions on setting up a Lavalink node on bare metal, look [here](https://lavalink.dev/getting-started/), and for instructions on the LavaSrc plugin, look [here](https://github.com/topi314/LavaSrc).
<br>
*P.S. Only the Deezer/SoundCloud sources/search providers are needed.*

It is also highly recommended to setup IPv6 rotation in order to avoid blocks and other issues. There are helpful guides for this both [here](https://blog.arbjerg.dev/2020/3/tunnelbroker-with-lavalink) and [here](https://gist.github.com/Drapersniper/11fee08f91ea7174e0d8af12496f3443).

An example of my personal `application.yml` file can be found [here](https://github.com/PacketParker/Guava/blob/main/application.yml.example).

<br>
<br>

If you have any questions, feel free to email at [contact@pkrm.dev](mailto:contact@pkrm.dev). Thank you for checking out Guava, and happy coding.

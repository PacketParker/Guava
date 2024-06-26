import configparser
import re
import validators
import sys
import discord
import openai
import logging
from colorlog import ColoredFormatter

log_level = logging.DEBUG
log_format = (
    "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
)

logging.root.setLevel(log_level)
formatter = ColoredFormatter(log_format)

stream = logging.StreamHandler()
stream.setLevel(log_level)
stream.setFormatter(formatter)

LOG = logging.getLogger("pythonConfig")
LOG.setLevel(log_level)
LOG.addHandler(stream)

TOKEN = None
BOT_COLOR = None
BOT_INVITE_LINK = None
FEEDBACK_CHANNEL_ID = None
BUG_CHANNEL_ID = None
SPOTIFY_CLIENT_ID = None
SPOTIFY_CLIENT_SECRET = None
CLIENT = None
LAVALINK_HOST = None
LAVALINK_PORT = None
LAVALINK_PASSWORD = None

"""
Load the config.ini file and return the contents for validation or
create a new templated config.ini file if it doesn't exist.
"""


def load_config():
    try:
        with open("config.ini", "r") as f:
            file_contents = f.read()
            return file_contents

    except FileNotFoundError:
        config = configparser.ConfigParser()
        config["BOT_INFO"] = {
            "TOKEN": "",
            "BOT_COLOR": "",
            "BOT_INVITE_LINK": "",
            "FEEDBACK_CHANNEL_ID": "",
            "BUG_CHANNEL_ID": "",
        }

        config["SPOTIFY"] = {
            "SPOTIFY_CLIENT_ID": "",
            "SPOTIFY_CLIENT_SECRET": "",
        }

        config["OPENAI"] = {
            "OPENAI_API_KEY": "",
        }

        config["LAVALINK"] = {
            "HOST": "",
            "PORT": "",
            "PASSWORD": "",
        }

        with open("config.ini", "w") as configfile:
            config.write(configfile)

        sys.exit(
            LOG.critical(
                "Configuration file `config.ini` has been generated. Please fill out all of the necessary information. Refer to the docs for information on what a specific configuration option is."
            )
        )


"""
Validate all of the options in the config.ini file.
"""


def validate_config(file_contents):
    global TOKEN, BOT_COLOR, BOT_INVITE_LINK, FEEDBACK_CHANNEL_ID, BUG_CHANNEL_ID, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, CLIENT, LAVALINK_HOST, LAVALINK_PORT, LAVALINK_PASSWORD
    config = configparser.ConfigParser()
    config.read_string(file_contents)

    hex_pattern_one = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    hex_pattern_two = "^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"

    errors = 0

    # Make sure all sections are present
    if ["BOT_INFO", "SPOTIFY", "OPENAI", "LAVALINK"] != config.sections():
        sys.exit(
            LOG.critical(
                "Missing sections in config.ini file. Delete the file and re-run the bot to generate a blank config.ini file."
            )
        )

    if ["token","bot_color","bot_invite_link", "feedback_channel_id","bug_channel_id",] != config.options("BOT_INFO"):
        sys.exit(
            LOG.critical(
                "Missing options in BOT_INFO section of config.ini file. Delete the file and re-run the bot to generate a blank config.ini file."
            )
        )

    if ["spotify_client_id", "spotify_client_secret"] != config.options("SPOTIFY"):
        sys.exit(
            LOG.critical(
                "Missing options in SPOTIFY section of config.ini file. Delete the file and re-run the bot to generate a blank config.ini file."
            )
        )

    if ["openai_api_key"] != config.options("OPENAI"):
        sys.exit(
            LOG.critical(
                "Missing options in OPENAI section of config.ini file. Delete the file and re-run the bot to generate a blank config.ini file."
            )
        )

    if ["host", "port", "password"] != config.options("LAVALINK"):
        sys.exit(
            LOG.critical(
                "Missing options in LAVALINK section of config.ini file. Delete the file and re-run the bot to generate a blank config.ini file."
            )
        )

    # Make sure BOT_COLOR is a valid hex color
    if not bool(re.match(hex_pattern_one, config["BOT_INFO"]["BOT_COLOR"])) and not bool(re.match(hex_pattern_two, config["BOT_INFO"]["BOT_COLOR"])):
        LOG.error("BOT_COLOR is not a valid hex color.")
        errors += 1
    else:
        BOT_COLOR = discord.Color(int((config["BOT_INFO"]["BOT_COLOR"]).replace("#", ""), 16))

    # Make sure BOT_INVITE_LINK is a valid URL
    if not validators.url(config["BOT_INFO"]["BOT_INVITE_LINK"]):
        LOG.error("BOT_INVITE_LINK is not a valid URL.")
        errors += 1
    else:
        BOT_INVITE_LINK = config["BOT_INFO"]["BOT_INVITE_LINK"]

    # Make sure FEEDBACK_CHANNEL_ID is either exactly 0 or 19 characters long
    if len(config["BOT_INFO"]["FEEDBACK_CHANNEL_ID"]) != 0:
        if len(config["BOT_INFO"]["FEEDBACK_CHANNEL_ID"]) != 19:
            LOG.error("FEEDBACK_CHANNEL_ID is not a valid Discord channel ID.")
            errors += 1
        else:
            FEEDBACK_CHANNEL_ID = int(config["BOT_INFO"]["FEEDBACK_CHANNEL_ID"])

    # Make sure BUG_CHANNEL_ID is either exactly 0 or 19 characters long
    if len(config["BOT_INFO"]["BUG_CHANNEL_ID"]) != 0:
        if len(config["BOT_INFO"]["BUG_CHANNEL_ID"]) != 19:
            LOG.error("BUG_CHANNEL_ID is not a valid Discord channel ID.")
            errors += 1
        else:
            BUG_CHANNEL_ID = int(config["BOT_INFO"]["BUG_CHANNEL_ID"])

    # Assign the rest of the variables
    TOKEN = config["BOT_INFO"]["TOKEN"]
    SPOTIFY_CLIENT_ID = config["SPOTIFY"]["SPOTIFY_CLIENT_ID"]
    SPOTIFY_CLIENT_SECRET = config["SPOTIFY"]["SPOTIFY_CLIENT_SECRET"]
    CLIENT = openai.OpenAI(api_key=config["OPENAI"]["OPENAI_API_KEY"])
    LAVALINK_HOST = config["LAVALINK"]["HOST"]
    LAVALINK_PORT = config["LAVALINK"]["PORT"]
    LAVALINK_PASSWORD = config["LAVALINK"]["PASSWORD"]

    if errors > 0:
        sys.exit(
            LOG.critical(
                f"Found {errors} error(s) in the config.ini file. Please fix them and try again."
            )
        )
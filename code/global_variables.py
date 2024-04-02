import configparser
import logging
from colorlog import ColoredFormatter
import discord


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

try:
    with open("config.ini", "r") as f:
        file_contents = f.read()
except FileNotFoundError:
    config = configparser.ConfigParser()
    config["BOT_INFO"] = {
        "TOKEN": "",
        "BOT_COLOR": "",
    }

    config["LAVALINK"] = {"HOST": "", "PORT": "", "PASSWORD": ""}

    with open("config.ini", "w") as configfile:
        config.write(configfile)

    LOG.error(
        "Configuration file `config.ini` has been generated. Please fill out all of the necessary information. Refer to the docs for information on what a specific configuration option is."
    )
    exit()


config = configparser.ConfigParser()
config.read_string(file_contents)

BOT_TOKEN = config["BOT_INFO"]["TOKEN"]
BOT_COLOR = discord.Color(int((config["BOT_INFO"]["BOT_COLOR"]).replace("#", ""), 16))
FEEDBACK_CHANNEL_ID = int(config["BOT_INFO"]["FEEDBACK_CHANNEL_ID"])
BUG_CHANNEL_ID = int(config["BOT_INFO"]["BUG_CHANNEL_ID"])

LAVALINK_HOST = config["LAVALINK"]["HOST"]
LAVALINK_PORT = config["LAVALINK"]["PORT"]
LAVALINK_PASSWORD = config["LAVALINK"]["PASSWORD"]

import configparser
import re
import validators

from global_variables import LOG


pattern_1 = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
pattern_2 = "^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"


def validate_config(file_contents):
    config = configparser.ConfigParser()
    config.read_string(file_contents)

    errors = 0

    try:
        # Validate TOKEN
        if not config["BOT_INFO"]["TOKEN"]:
            LOG.critical("TOKEN has not been set.")
            errors += 1
        # Validate BOT_COLOR
        if not config["BOT_INFO"]["BOT_COLOR"]:
            LOG.critical("BOT_COLOR has not been set.")
            errors += 1

        elif not bool(
            re.match(pattern_1, config["BOT_INFO"]["BOT_COLOR"])
        ) and not bool(re.match(pattern_2, config["BOT_INFO"]["BOT_COLOR"])):
            LOG.critical("BOT_COLOR is not a valid hex color.")
            errors += 1
        # Validate FEEDBACK_CHANNEL_ID
        if not config["BOT_INFO"]["FEEDBACK_CHANNEL_ID"]:
            LOG.critical("FEEDBACK_CHANNEL_ID has not been set.")
            errors += 1

        elif len(config["BOT_INFO"]["FEEDBACK_CHANNEL_ID"]) != 19:
            LOG.critical("FEEDBACK_CHANNEL_ID is not a valid Discord channel ID.")
            errors += 1
        # Validate SPOTIFY_CLIENT_ID
        if not config["BOT_INFO"]["SPOTIFY_CLIENT_ID"]:
            LOG.critical("SPOTIFY_CLIENT_ID has not been set.")
            errors += 1
        # Validate SPOTIFY_CLIENT_SECRET
        if not config["BOT_INFO"]["SPOTIFY_CLIENT_SECRET"]:
            LOG.critical("SPOTIFY_CLIENT_SECRET has not been set.")
            errors += 1
        # Validate BUG_CHANNEL_ID
        if not config["BOT_INFO"]["BUG_CHANNEL_ID"]:
            LOG.critical("BUG_CHANNEL_ID has not been set.")
            errors += 1

        elif len(config["BOT_INFO"]["BUG_CHANNEL_ID"]) != 19:
            LOG.critical("BUG_CHANNEL_ID is not a valid Discord channel ID.")
            errors += 1
        # Validate BOT_INVITE_LINK
        if not config["BOT_INFO"]["BOT_INVITE_LINK"]:
            LOG.critical("BOT_INVITE_LINK has not been set.")
            errors += 1

        elif not validators.url(config["BOT_INFO"]["BOT_INVITE_LINK"]):
            LOG.critical("BOT_INVITE_LINK is not a valid URL.")
            errors += 1

        # Validate LAVALINK
        # Validate HOST
        if not config["LAVALINK"]["HOST"]:
            LOG.critical("HOST has not been set.")
            errors += 1
        # Validate PORT
        if not config["LAVALINK"]["PORT"]:
            LOG.critical("PORT has not been set.")
            errors += 1
        # Validate PASSWORD
        if not config["LAVALINK"]["PASSWORD"]:
            LOG.critical("HOST has not been set.")
            errors += 1

        if errors > 0:
            LOG.critical(
                "Configuration checks failed. Correct your config.ini file and run again."
            )
            exit()

        else:
            LOG.info("Configuration checks passed. Starting bot.")

    except KeyError:
        LOG.critical(
            "You are missing at least one of the configuration options from your config.ini file. In order to regenerate this file with all of the proper options, please delete it and re-run the `bot.py` file."
        )
        exit()


def create_config():
    try:
        with open("config.ini", "r") as f:
            file_contents = f.read()
            validate_config(file_contents)

    except FileNotFoundError:
        config = configparser.ConfigParser()
        config["BOT_INFO"] = {
            "TOKEN": "",
            "BOT_COLOR": "",
            "FEEDBACK_CHANNEL_ID": "",
            "SPOTIFY_CLIENT_ID": "",
            "SPOTIFY_CLIENT_SECRET": "",
            "BUG_CHANNEL_ID": "",
        }

        config["LAVALINK"] = {"HOST": "", "PORT": "", "PASSWORD": ""}

        with open("config.ini", "w") as configfile:
            config.write(configfile)

        LOG.error(
            "Configuration file `config.ini` has been generated. Please fill out all of the necessary information. Refer to the docs for information on what a specific configuration option is."
        )
        exit()

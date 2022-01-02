import decouple
import nextcord
from nextcord.ext import commands
import sys

from automoji import Automoji
from am_logging import logger
from am_db import db_conn


def main():
    # Gets bot intents.
    intents = nextcord.Intents.default()
    intents.members = True

    # Initializes the bot.
    bot = Automoji(command_prefix="!", intents=intents)

    # Loads extensions into the bot.
    extensions = ["cogs.user_emojis", "cogs.quotes"]
    for ext in extensions:
        try:
            bot.load_extension(ext)
        except commands.ExtensionError as e:
            logger.warning(e)

    # Runs the bot using the token specified as an environment variable.
    try:
        token = decouple.config("TOKEN")
    except decouple.UndefinedValueError as e:
        logger.error(e)
        print("An error has occurred. See discord.log for more details.\nExiting")
        sys.exit(1)

    try:
        bot.run(token)
    except (
        nextcord.LoginFailure,
        nextcord.HTTPException,
        nextcord.GatewayNotFound,
        nextcord.ConnectionClosed,
    ) as e:
        logger.error(e)
        print("An error has occurred. See discord.log for more details.\nExiting")
        sys.exit(1)

    # Closes the connection to the database.
    db_conn.close()


if __name__ == "__main__":
    main()

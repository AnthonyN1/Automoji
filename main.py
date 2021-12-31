import decouple
import discord
from discord.ext import commands
import sys

from automoji import Automoji
from am_logging import logger


def main():
    # Gets bot intents.
    intents = discord.Intents.default()
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
        discord.LoginFailure,
        discord.HTTPException,
        discord.GatewayNotFound,
        discord.ConnectionClosed,
    ) as e:
        logger.error(e)
        print("An error has occurred. See discord.log for more details.\nExiting")
        sys.exit(1)


if __name__ == "__main__":
    main()

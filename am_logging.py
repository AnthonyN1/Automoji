import logging


# Adds logger.
logger = logging.getLogger("discord")
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s :: %(levelname)-8s :: %(message)s"))
logger.addHandler(handler)

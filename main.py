from decouple import config
import discord
import discord.ext
import sys

from automoji import Automoji


def main():
	# Gets bot intents.
	intents = discord.Intents.default()
	intents.members = True

	# Initializes the bot.
	bot = Automoji(command_prefix="!", intents=intents)

	# Runs the bot using the token (specified as an environment variable).
	token = config("TOKEN")
	try:
		bot.run(token)
	except (discord.LoginFailure, discord.HTTPException):
		print("Something went wrong. The bot was unable to login successfully.")
		sys.exit(1)
		


if __name__ == "__main__":
	main()

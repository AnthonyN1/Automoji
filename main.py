from decouple import config
import discord
import discord.ext

from automoji import Automoji


def main():
	# Gets bot intents.
	intents = discord.Intents.default()
	intents.members = True

	# Initializes the bot.
	bot = Automoji(command_prefix="!", intents=intents)

	# Runs the bot using the token (specified as an environment variable).
	token = config("TOKEN")
	bot.run(token)


if __name__ == "__main__":
	main()

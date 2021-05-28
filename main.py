from decouple import config
import discord
import discord.ext

from automoji import Automoji


def main():
	intents = discord.Intents.default()
	intents.members = True

	bot = Automoji(command_prefix="!", intents=intents)

	token = config("TOKEN")
	bot.run(token)


if __name__ == "__main__":
	main()

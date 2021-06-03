import decouple
import discord
from discord.ext import commands
import sys

from automoji import Automoji


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
			print(f"WARNING: unable to load the extension {e.name}")

	# Runs the bot using the token specified as an environment variable.
	try:
		token = decouple.config("TOKEN")
	except decouple.UndefinedValueError:
		print("ERROR: environment variable 'TOKEN' not set\nExiting...")
		sys.exit(1)
	
	try:
		bot.run(token)
	except discord.LoginFailure:
		print("ERROR: unable to login using the provided credentials\nExiting...")
		sys.exit(1)
	except discord.HTTPException as e:
		print(f"ERROR: an HTTP exception has occured (status code {e.status})\nExiting...")
		sys.exit(1)
	except discord.GatewayNotFound:
		print("ERROR: unable to find the gateway hub\nExiting...")
		sys.exit(1)
	except discord.ConnectionClosed as e:
		print(f"ERROR: connection closed ({e.reason})\nExiting...")
		sys.exit(1)


if __name__ == "__main__":
	main()

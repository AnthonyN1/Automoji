import discord
from discord.ext import commands
import emoji


class Automoji(commands.Bot):
	# Class constructor.
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# Constructs a dictionary, where the keys are Users, and the values are strings 
		# representing emojis.
		self.user_emojis = {}
	
	
	async def on_message(self, message: discord.Message):
		# Avoids the bot recursing through its own messages.
		if message.author.id == self.user.id:
			return
		
		# Reacts to the user's message with their emoji.
		await self.react_user_emoji(message)

		await self.process_commands(message)
	
	
	# Reacts to a user's message with their emoji.
	async def react_user_emoji(self, message: discord.Message):
		try:
			# Gets the user's emoji.
			user = message.author
			em = self.user_emojis[user]
		except KeyError:
			# If the user doesn't have an emoji, don't do anything.
			return
		
		# Reacts to the user's message with their emoji.
		try:
			await message.add_reaction(em)
		except discord.DiscordException as e:
			self.add_reaction_error(e)
	

	# Prints warning messages to the console based on the type of exception caught when adding a 
	# reaction.
	def add_reaction_error(self, error: discord.DiscordException):
		if isinstance(error, discord.Forbidden):
			print("WARNING: received status code 403 (Forbidden)")
			print("         unable to react with an emoji")
			print("         requires permissions 'read_message_history' and 'add_reactions'")
		elif isinstance(error, discord.NotFound):
			print("WARNING: received status code 404 (Not Found)")
			print("         unable to react with an emoji")
			print("         specified emoji was not found")
		elif isinstance(error, discord.HTTPException):
			print(f"WARNING: an HTTP exception has occured (status code {error.status})")
			print("         unable to react with an emoji.")
		elif isinstance(error, discord.InvalidArgument):
			print("WARNING: invalid argument when reacting with an emoji")
	
	# Determines if 'arg' is a valid emoji.
	# A valid emoji can be: (1) unicode, (2) custom to the current guild, or (3) custom to a guild 
	# outside the current one (e.g. Discord Nitro).
	def is_emoji(self, guild: discord.Guild, arg: str):
		# (1) Unicode emojis
		if emoji.emoji_count(arg) == 1: return True

		# (2) Custom emojis in the current guild
		if (guild != None) and (any(arg == str(em) for em in guild.emojis)): return True

		# TODO: (3) Custom emojis to a guild outside the current one

		return False

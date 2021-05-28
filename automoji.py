import discord
from discord.ext import commands


class Automoji(commands.Bot):
	# Class constructor.
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# Constructs a dictionary, where the keys are Users, and the values are strings 
		# representing emojis.
		self.user_emojis = {}
	
	
	async def on_message(self, message: discord.Message):
		await self.process_commands(message)

		# Avoids the bot recursing through its own messages.
		if message.author.id == self.user.id:
			return
		
		# Reacts to the user's message with their emoji.
		await self.react_user_emoji(message)
	
	
	# Reacts to a user's message with their emoji.
	async def react_user_emoji(self, message: discord.Message):
		try:
			# Gets the user's emoji.
			user = message.author
			emoji = self.user_emojis[user]
		except KeyError:
			# If the user doesn't have an emoji, don't do anything.
			return
		
		# Reacts to the user's message with their emoji.
		try:
			await message.add_reaction(emoji)
		except discord.Forbidden:
			print("WARNING: received status code 403 (Forbidden)")
			print("         unable to react with an emoji")
			print("         requires permissions 'read_message_history' and 'add_reactions'")
		except discord.NotFound:
			print("WARNING: received status code 404 (Not Found)")
			print("         unable to react with an emoji")
			print("         specified emoji was not found")
		except discord.HTTPException as e:
			print(f"WARNING: an HTTP exception has occured (status code {e.status})")
			print("         unable to react with an emoji.")
		except discord.InvalidArgument:
			print("WARNING: invalid argument when reacting with an emoji")

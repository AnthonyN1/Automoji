from decouple import config
import discord
from discord.ext import commands


class Automoji(commands.Bot):
	# Class constructor.
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# Creates a dictionary, where the keys are Users, and the values are PartialEmojis.
		self.user_emojis = {}
	
	
	async def on_message(self, message: discord.Message):
		await self.process_commands(message)

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

			# Reacts to the user's message with their emoji.
			await message.add_reaction(emoji)
		except KeyError:
			# If the user doesn't have an emoji, don't do anything.
			return

from decouple import config
import discord
from discord.ext import commands


class Automoji(commands.Bot):
	# Class constructor.
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# Creates a dictionary, where the keys are Users, and the values are PartialEmojis.
		self.user_emojis = {}
		self.ue_msg = None
	

	async def on_ready(self):
		await self.send_ue_msg()
	
	async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
		if payload.message_id == self.ue_msg.id:
			await self.add_user_emoji(payload)
	
	async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
		if payload.message_id == self.ue_msg.id:
			self.remove_user_emoji(payload)
	
	async def on_message(self, message: discord.Message):
		if message.author.id == self.user.id:
			return
		
		await self.react_user_emoji(message)
	

	# Sends the user_emojis message to the specified channel, and stores the message ID.
	async def send_ue_msg(self):
		channel_id = config("CHANNEL_ID", cast=int)
		channel = self.get_channel(channel_id)

		ue_msg_str = "React to this message to get your custom emoji!\n- I'll react to every message you send with this emoji.\n- You may only have one emoji.\n- Please wait 5 seconds after reacting before messaging."
		self.ue_msg = await channel.send(ue_msg_str)
	
	# Adds to the user_emojis dictionary when a user reacts to ue_msg.
	async def add_user_emoji(self, payload: discord.RawReactionActionEvent):
		# Gets the user and their emoji
		guild = self.get_guild(payload.guild_id)
		user = guild.get_member(payload.user_id)
		emoji = payload.emoji

		# If the user already has an emoji, overwrites it, and removes their previous reaction.
		if user in self.user_emojis:
			prev_emoji = self.user_emojis[user]
			await self.ue_msg.remove_reaction(prev_emoji, user)
		
		# Adds the User and their PartialEmoji to the dictionary.
		self.user_emojis[user] = emoji
	
	# Removes from the user_emojis dictionary when a user removes their reaction from ue_msg.
	def remove_user_emoji(self, payload: discord.RawReactionActionEvent):
		# Removes the user from the dictionary.
		guild = self.get_guild(payload.guild_id)
		user = guild.get_member(payload.user_id)
		self.user_emojis.pop(user)
	
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


def main():
	intents = discord.Intents.default()
	intents.members = True

	bot = Automoji(command_prefix="!", intents=intents)

	token = config("TOKEN")
	bot.run(token)

if __name__ == "__main__":
	main()

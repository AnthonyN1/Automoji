import discord
from discord.ext import commands
import emoji


class Automoji(commands.Bot):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# Constructs a dictionary, where the keys are Guilds, and the values are dictionaries. 
		# In the sub-dictionaries, the keys are Members, and the values are strings that represent 
		# emojis.
		self.user_emojis = {}
		self.quotesChannel = None
		self.quotes = list()
		self.robot_emoji = "\U0001F916"
	
	async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
		if isinstance(error, commands.CommandNotFound):
			await self.custom_send(ctx, "I couldn't recognize that command. Please see '!help' for a list of commands.")
	
	async def on_message(self, message: discord.Message):
		# Avoids the bot recursing through its own messages.
		if message.author.id == self.user.id:
			return
		
		self.add_quote(message)
		
		# Reacts to the user's message with their emoji.
		await self.react_user_emoji(message)

		#TODO: add quote to quotes list
		await self.process_commands(message)
		
		
	
	async def on_ready(self):
		print("Automoji is now online!")
	

	# Reacts to a message using the robot emoji.
	async def bot_react(self, message: discord.Message):
		try:
			await message.add_reaction(self.robot_emoji)
		except discord.DiscordException as e:
			self.add_reaction_error(e)
	
	# Sends a message to the specified channel, and catches any thrown exceptions.
	async def custom_send(self, ctx: commands.Context, msg: str):
		try:
			await ctx.send(msg)
		except discord.HTTPException as e:
			self.send_error(e)
	
	# Reacts to a user's message with their emoji.
	async def react_user_emoji(self, message: discord.Message):
		try:
			# Gets the user's emoji.
			user = message.author
			em = self.user_emojis[message.guild][user]
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
	
	# Prints warning messages to the console based on the type of exception caught when sending a 
	# message.
	def send_error(self, error: discord.HTTPException):
		if isinstance(error, discord.Forbidden):
			print("WARNING: received status code 403 (Forbidden)")
			print("         unable to send a message")
			print("         requires permission 'send_messages'")
		else:
			print(f"WARNING: an HTTP exception has occured (status code {error.status})")
			print("         unable to send a message.")
	

	# Determines if 'arg' is a valid emoji.
	# A valid emoji can be: (1) unicode, (2) custom to the current guild
	def is_emoji(self, guild: discord.Guild, arg: str):
		# (1) Unicode emojis
		if emoji.emoji_count(arg) == 1: return True

		# (2) Custom emojis in the current guild
		if (guild != None) and (any(arg == str(em) for em in guild.emojis)): return True

		return False
	
	# Determines if 'message' is a quote
	# A valid quote is one that does not have embeds or mentions and is not from or for the bot
	def is_quote(self, message: discord.Message):
		#Checks if it is a message from the bot
		if message.author.id == self.user.id: return False
		
		#Checks if the message has any mentions
		if len(message.mentions) > 0 or len(message.role_mentions) > 0 or len(message.channel_mentions) > 0: return False
		
		#Checks if the message has any embeds
		if len(message.embeds) > 0: return False
		
		#Check if the message contains an @everyone
		#if message.mention_everyone: return False
		
		#TODO: try and find a way to exclude commands
		
		return True
	
	#Adds a quote to quote list if valid
	def add_quote(self, message: discord.Message):
		#Checks if quotesChannel is called and if quotes Channel is the message's channel
		if self.quotesChannel == None or message.channel != self.quotesChannel:
			return
		
		#Checks if the message is a valid quote
		if self.is_quote(message):
			self.quotes.append(message)
		else:
			print(f"Omitted: {message.content} from quote list")
			return
	
	
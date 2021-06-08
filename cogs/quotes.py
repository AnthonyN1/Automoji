import discord
from discord.ext import commands
import random


class Quotes(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.cog_errors = [commands.NoPrivateMessage, commands.MissingRequiredArgument, commands.TooManyArguments]
	

	# Registers as a commands.Check() to all commands in this Cog.
	def cog_check(self, ctx: commands.Context):
		# All commands in this Cog can only be used in guilds.
		if ctx.guild is None: raise commands.NoPrivateMessage
		
		return True
	
	# Catches any errors not dealt with in the commands' individual error handlers.
	async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
		if isinstance(error, commands.NoPrivateMessage):
			await self.bot.custom_send(ctx, "That command doesn't work in DMs!")
		elif isinstance(error, (commands.MissingRequiredArgument, commands.TooManyArguments)):
			await self.bot.custom_send(ctx, f"Invalid number of arguments. Please see '!help {ctx.command}'.")
		else:
			print(error)

	@commands.command(name="setQuoteChannel")
	async def set_quote_channel(self, ctx: commands.Context, arg1: str):
		"""
		Sets the channel for quotes
		- Everytime a user requests a quote, Automoji will send a random message from this channel
	
		expects: channel name
		
		Failure conditions:
		- You pass too little or too many arguments
		- The quote channel is already set
		- There are no messages in the quote channel
		- There is not a channel with that name
		- There are multiple channels with that name
		"""
		if ctx.guild not in self.bot.quotesChannels:
			self.bot.quotesChannels[ctx.guild] = None
			
		if ctx.guild not in self.bot.quotes:
			self.bot.quotes[ctx.guild] = list()
			
		if self.bot.quotesChannels[ctx.guild] != None:
			await self.bot.custom_send(ctx, "Quote channel is already set! Try removing the channel.")
			return
		
		quoteChannel = None
		# Search for the channel
		for c in ctx.guild.text_channels:
			if arg1 == c.name:
				if quoteChannel != None:
					await self.bot.custom_send(ctx, "There are multiple channels with that name! Maybe rename one?")
					return
				quoteChannel = c
		
		# If the channel is not found, return
		if quoteChannel == None:
			await self.bot.custom_send(ctx, f"Sorry, {arg1} is not a valid channel!")
			return
		
		quoteList = list()
		async for m in quoteChannel.history():
			if m.author.id != self.bot.user.id: quoteList.append(m)
			else: print(f"Omitted: {m.clean_content} from quote list")
			
		if len(quoteList) <= 0:
			await self.bot.custom_send(ctx, "Selected channel does not contain any valid quotes")
			return
		
		
		self.bot.quotesChannels[ctx.guild] = quoteChannel
		self.bot.quotes[ctx.guild] = quoteList
		await self.bot.bot_react(ctx.message)
	
	# Catches a discord Forbidden error
	@set_quote_channel.error
	async def set_quote_channel_error(self, ctx: commands.Context, error: commands.CommandError):
		if isinstance(error, discord.Forbidden):
			print("WARNING: received status code 403 (Forbidden)")
			print("         unable to read message history")
			print("         requires permission 'read_message_history'")
		elif type(error) not in self.cog_errors:
			print(f"Caught unexpected exception at set_quote_channel(): {type(error)}")
			
	@commands.command(name="removeQuoteChannel")
	async def remove_quote_channel(self, ctx: commands.Context):
		"""
		Removes the channels for quotes
		- When called, Automoji will remove the current quote channel
		
		expects: nothing
		
		Failure conditions:
		- Any argument is passed
		- The quote channel is not set
		"""
		if ctx.guild not in self.bot.quotesChannels or self.bot.quotesChannels[ctx.guild] == None:
			await self.bot.custom_send(ctx, "No quote channel to remove!")
			return
		
		self.bot.quotesChannels[ctx.guild] = None
		self.bot.quotes[ctx.guild].clear()
		await self.bot.bot_react(ctx.message)
	
	# No explicitly caught exceptions.
	@remove_quote_channel.error
	async def remove_quote_channel_error(self, ctx: commands.Context, error: commands.CommandError):
		if type(error) not in self.cog_errors:
			print(f"Caught unexpected exception at remove_quote_channel(): {type(error)}")
			
	@commands.command(name="getQuote")
	async def get_quote(self, ctx: commands.context):
		"""
		Grabs a quote
		- When called, Automoji will grab a random message from the set quote channel
		
		expects: nothing
		
		Failure conditions:
		- Any argument is passed
		- The quote channel is not set
		- The quote channel has no available quote messages
		"""
		if ctx.guild not in self.bot.quotesChannels or self.bot.quotesChannels[ctx.guild] == None: 
			await self.bot.custom_send(ctx, "No quote channel set!")
			return
		try:
			randomMessage = random.choice(self.bot.quotes[ctx.guild])
		except IndexError:
			await self.bot.custom_send(ctx, "Quotes channel contains no valid quotes!")
			return
		
		# Sends a clean version of the message to the channel
		await self.bot.custom_send(ctx, randomMessage.clean_content)
	
	# No explicitly caught exceptions.
	@get_quote.error
	async def get_quote_error(self, ctx: commands.Context, error: commands.CommandError):
		if type(error) not in self.cog_errors:
			print(f"Caught unexpected exception at get_quote(): {type(error)}")


# Required function for an extension.
def setup(bot: commands.Bot):
	bot.add_cog(Quotes(bot))
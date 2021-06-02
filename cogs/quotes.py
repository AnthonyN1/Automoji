import discord
from discord.ext import commands

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

	@commands.command(name="setQuoteChannel")
	async def set_quote_channel(self, ctx: commands.Context, arg1: str, arg2: str = None):
		"""
		Sets the channel for quotes
		- Everytime a user requests a quote, Automoji will send a random message from this channel
	
		expects: channel name and optional channel category
		
		Failure conditions:
		- You pass too little or too many arguments
		- The quote channel is already set
		- There are no messages in the quote channel
		- There is not a channel with that name
		- There are multiple channels with that name
		"""
	
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
	
	@commands.command(name="getQuote")
	async def get_quote(self, ctx: commands.context):
		"""
		Grabs a quote
		- When called, Automoji will grab a random message from the set quote channel
		
		expects: nothing
		
		Failure conditions:
		- Any argument is passed
		- The quote channel is not set
		"""

# Required function for an extension.
def setup(bot: commands.Bot):
	bot.add_cog(Quotes(bot))
from discord.ext import commands


class UserEmojis(commands.Cog):
	# Class constructor.
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.robot_emoji = "\U0001F916"
	

	# Command: !addUserEmoji <emoji>
	# Assigns the user to the specified emoji. For every message the user sends, the bot will 
	# react with that emoji.
	@commands.command(name="addUserEmoji", ignore_extra=False)
	async def add_user_emoji(self, ctx: commands.Context, arg: str):
		# If 'arg' isn't an emoji, sends an error message.
		if not self.bot.is_emoji(ctx.guild, arg):
			await ctx.send("Invalid argument. Are you sure that's an emoji?")
			return
		
		# Adds the user and their emoji to the dictionary.
		self.bot.user_emojis[ctx.author] = arg

		# Reacts to the user's message.
		try:
			await ctx.message.add_reaction(self.robot_emoji)
		except Exception as e:
			self.bot.add_reaction_error(e)
	
	# Explicitly caught exceptions: MissingRequiredArgument, TooManyArguments
	@add_user_emoji.error
	async def add_user_emoji_error(self, ctx: commands.Context, error: commands.CommandError):
		if isinstance(error, (commands.MissingRequiredArgument, commands.TooManyArguments)):
			await ctx.send("Invalid number of arguments. Please see '!help addUserEmoji'")
	

	# Command: !removeUserEmoji
	# Unassigns a user from their emoji. 
	@commands.command(name="removeUserEmoji")
	async def remove_user_emoji(self, ctx: commands.Context):
		self.bot.user_emojis.pop(ctx.author)

		try:
			await ctx.message.add_reaction(self.robot_emoji)
		except Exception as e:
			self.bot.add_reaction_error(e)


# Required function for an extension.
def setup(bot: commands.Bot):
	bot.add_cog(UserEmojis(bot))

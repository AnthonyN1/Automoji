import discord
from discord.ext import commands


class UserEmojis(commands.Cog):
	# Class constructor.
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	

	# Command: !addUserEmoji <emoji>
	# Assigns the user to the specified emoji. For every message the user sends, the bot will 
	# react with that emoji.
	@commands.command(name="addUserEmoji", ignore_extra=False)
	async def add_user_emoji(self, ctx: commands.Context, arg: str):
		# If 'arg' isn't an emoji, sends an error message.
		if not self.bot.is_emoji(ctx.guild, arg):
			await self.bot.custom_send(ctx, "Invalid argument. Are you sure that's an emoji?")
			return
		
		# If the user already has an emoji, sends an error message.
		if ctx.author in self.bot.user_emojis:
			await self.bot.custom_send(ctx, "You already have an emoji! Please use '!removeUserEmoji' first.")
			return
		
		# Adds the user and their emoji to the dictionary.
		self.bot.user_emojis[ctx.author] = arg

		# Reacts to the user's message.
		await self.bot.bot_react(ctx.message)
	
	# Explicitly caught exceptions: MissingRequiredArgument, TooManyArguments
	@add_user_emoji.error
	async def add_user_emoji_error(self, ctx: commands.Context, error: commands.CommandError):
		if isinstance(error, (commands.MissingRequiredArgument, commands.TooManyArguments)):
			await self.bot.custom_send(ctx, "Invalid number of arguments. Please see '!help addUserEmoji'.")
		else:
			print(f"Caught unexpected exception at add_user_emoji(): {type(error)}")
	

	# Command: !removeUserEmoji
	# Unassigns a user from their emoji. 
	@commands.command(name="removeUserEmoji", ignore_extra=False)
	async def remove_user_emoji(self, ctx: commands.Context):
		# If the user doesn't have an emoji, sends an error message.
		if ctx.author not in self.bot.user_emojis:
			await self.bot.custom_send(ctx, "You don't have an emoji to remove!")
			return
		
		# Removes the user from the dictionary.
		self.bot.user_emojis.pop(ctx.author)

		# Reacts to the user's message.
		await self.bot.bot_react(ctx.message)
	
	# Explicitly caught exceptions: TooManyArguments
	@remove_user_emoji.error
	async def remove_user_emoji_error(self, ctx: commands.Context, error: commands.CommandError):
		if isinstance(error, commands.TooManyArguments):
			await self.bot.custom_send(ctx, "Invalid number of arguments. Please see '!help removeUserEmoji'.")
		else:
			print(f"Caught unexpected exception at remove_user_emoji(): {type(error)}")
	

	# Command: !getUserEmoji [member]
	# Gets the specified user's emoji and sends it to the channel.
	@commands.command(name="getUserEmoji", ignore_extra=False)
	async def get_user_emoji(self, ctx: commands.Context, member: discord.Member = None):
		# If the user doesn't specify a member, they default to being the member.
		if member == None:
			member = ctx.author
		
		# Gets the member's emoji.
		try:
			em = self.bot.user_emojis[member]
		except KeyError:
			await self.bot.custom_send(ctx, f"{member.name} doesn't have an emoji!")
			return
		
		# Sends the member's emoji to the channel.
		await self.bot.custom_send(ctx, f"{member.name}'s emoji is {em}!")
	
	# Explicitly caught exceptions: TooManyArguments, MemberNotFound
	@get_user_emoji.error
	async def get_user_emoji_error(self, ctx: commands.Context, error: commands.CommandError):
		if isinstance(error, commands.TooManyArguments):
			await self.bot.custom_send(ctx, "Invalid number of arguments. Please see '!help getUserEmoji'.")
		elif isinstance(error, commands.MemberNotFound):
			await self.bot.custom_send(ctx, "I couldn't find that member...")
		else:
			print(f"Caught unexpected exception at get_user_emoji(): {type(error)}")


# Required function for an extension.
def setup(bot: commands.Bot):
	bot.add_cog(UserEmojis(bot))

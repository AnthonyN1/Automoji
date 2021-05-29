import discord
from discord.ext import commands


class UserEmojis(commands.Cog, name="User Emojis", command_attrs=dict(ignore_extra=False)):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	

	@commands.command(name="addUserEmoji")
	async def add_user_emoji(self, ctx: commands.Context, arg: str):
		"""
		Adds an emoji to all of your messages
		- For every message you send in a channel Automoji has access to, Automoji will react to it with this emoji.
		
		Expects: one emoji
		
		Failure conditions:
		- You don't pass anything.
		- You pass more than one emoji.
		- You pass something other than an emoji.
		- There's already an emoji assigned to you.
		"""
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
	

	@commands.command(name="getUserEmoji")
	async def get_user_emoji(self, ctx: commands.Context, member: discord.Member = None):
		"""
		Gets a user's emoji
		- Automoji will send a message detailing the specified user's emoji.

		Expects: nothing, or one user
		- If you don't pass anything, the specified user defaults to you.
		- A user can be passed by:
			- user ID
			- mention
			- username#discriminator
			- username
			- nickname
		
		Failure conditions:
		- You pass more than one user.
		- You pass something that doesn't represent a user in this server.
		- You passed a user that doesn't have an emoji assigned to them.
		"""
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
			await self.bot.custom_send(ctx, "I couldn't find that user...")
		else:
			print(f"Caught unexpected exception at get_user_emoji(): {type(error)}")
	

	@commands.command(name="removeUserEmoji")
	async def remove_user_emoji(self, ctx: commands.Context):
		"""
		Removes your assigned emoji
		- Automoji will stop reacting to your messages with your emoji.

		Expects: nothing

		Failure conditions:
		- You pass something.
		- You don't have an emoji assigned to you.
		"""
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


# Required function for an extension.
def setup(bot: commands.Bot):
	bot.add_cog(UserEmojis(bot))

from discord.ext import commands


class UserEmojis(commands.Cog):
	# Class constructor.
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.robot_emoji = "\U0001F916"
	

	# Command: !addUserEmoji <emoji>
	# Assigns the user to the specified emoji. For every message the user sends, the bot will 
	# react with that emoji.
	@commands.command(name="addUserEmoji")
	async def add_user_emoji(self, ctx, emoji: str):
		self.bot.user_emojis[ctx.author] = emoji

		try:
			await ctx.message.add_reaction(self.robot_emoji)
		except Exception as e:
			self.bot.add_reaction_error(e)
	
	# Command: !removeUserEmoji
	# Removes the user's emoji. 
	@commands.command(name="removeUserEmoji")
	async def remove_user_emoji(self, ctx):
		self.bot.user_emojis.pop(ctx.author)

		try:
			await ctx.message.add_reaction(self.robot_emoji)
		except Exception as e:
			self.bot.add_reaction_error(e)


# Required function for an extension.
def setup(bot: commands.Bot):
	bot.add_cog(UserEmojis(bot))

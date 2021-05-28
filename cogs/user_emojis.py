from discord.ext import commands


class UserEmojis(commands.Cog):
	# Class constructor.
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.thumbs_up = '\N{THUMBS UP SIGN}'
	

	# Command: !addUserEmoji <emoji>
	# Assigns the user to the specified emoji. For every message the user sends, the bot will 
	# react with that emoji.
	@commands.command(name="addUserEmoji")
	async def add_user_emoji(self, ctx, emoji: str):
		self.bot.user_emojis[ctx.author] = emoji

		await ctx.message.add_reaction(self.thumbs_up)
	
	# Command: !removeUserEmoji
	# Removes the user's emoji. 
	@commands.command(name="removeUserEmoji")
	async def remove_user_emoji(self, ctx):
		self.bot.user_emojis.pop(ctx.author)

		await ctx.message.add_reaction(self.thumbs_up)


# Required function for an extension.
def setup(bot: commands.Bot):
	bot.add_cog(UserEmojis(bot))

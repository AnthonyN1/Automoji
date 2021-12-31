import discord
from discord.ext import commands

from am_logging import logger


class UserEmojis(
    commands.Cog, name="User Emojis", command_attrs=dict(ignore_extra=False)
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cog_errors = (
            commands.NoPrivateMessage,
            commands.MissingRequiredArgument,
            commands.TooManyArguments,
        )

    # Registers as a commands.Check() to all commands in this Cog.
    def cog_check(self, ctx):
        # All commands in this Cog can only be used in guilds.
        if ctx.guild is None:
            raise commands.NoPrivateMessage

        return True

    # Catches any errors not dealt with in the commands' individual error handlers.
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("That command doesn't work in DMs!")
        elif isinstance(error, self.cog_errors):
            await ctx.send("Invalid number of arguments.")

    @commands.command(name="addUserEmoji")
    async def add_user_emoji(self, ctx, emoji):
        """
        Adds an emoji to all of your messages

        * This is a SERVER-ONLY command.
        """
        # If 'arg' isn't an emoji, sends an error message.
        if not self.bot.is_emoji(ctx.guild, emoji):
            await ctx.send("Invalid argument. Are you sure that's an emoji?")
            return

        # If the guild isn't in the dictionary yet, adds it.
        if ctx.guild not in self.bot.user_emojis:
            self.bot.user_emojis[ctx.guild] = {}

        # If the user already has an emoji in this guild, sends an error message.
        if ctx.author in self.bot.user_emojis[ctx.guild]:
            await ctx.send(
                "You already have an emoji! Please use '!removeUserEmoji' first."
            )
            return

        # Adds the user and their emoji to the sub-dictionary.
        self.bot.user_emojis[ctx.guild][ctx.author] = emoji

        # Reacts to the user's message.
        await self.bot.bot_react(ctx.message)

    # No explicitly caught exceptions.
    @add_user_emoji.error
    async def add_user_emoji_error(self, ctx, error):
        if type(error) not in self.cog_errors:
            logger.warning(error)

    @commands.command(name="getUserEmoji")
    async def get_user_emoji(self, ctx, member: discord.Member = None):
        """
        Gets a user's emoji

        * This is a SERVER-ONLY command.
        """
        # If the user doesn't specify a member, they default to being the member.
        if member == None:
            member = ctx.author

        # Gets the member's emoji.
        try:
            emoji = self.bot.user_emojis[ctx.guild][member]
        except KeyError:
            await ctx.send(f"{member.name} doesn't have an emoji!")
            return

        # Sends the member's emoji to the channel.
        await ctx.send(f"{member.name}'s emoji is {emoji}!")

    # Explicitly caught exception: MemberNotFound
    @get_user_emoji.error
    async def get_user_emoji_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("I couldn't find that user...")
        elif type(error) not in self.cog_errors:
            logger.warning(error)

    @commands.command(name="removeUserEmoji")
    async def remove_user_emoji(self, ctx):
        """
        Removes your assigned emoji

        * This is a SERVER-ONLY command.
        """
        # Removes the user from the dictionary.
        try:
            self.bot.user_emojis[ctx.guild].pop(ctx.author)
        except KeyError:
            await ctx.send("You don't have an emoji to remove!")
            return

        # If the sub-dictionary is now empty, removes it from the dictionary.
        try:
            if len(self.bot.user_emojis[ctx.guild]) == 0:
                self.bot.user_emojis.pop(ctx.guild)
        except KeyError:
            pass

        # Reacts to the user's message.
        await self.bot.bot_react(ctx.message)

    # No explicitly caught exceptions.
    @remove_user_emoji.error
    async def remove_user_emoji_error(self, ctx, error):
        if type(error) not in self.cog_errors:
            logger.warning(error)


# Required function for an extension.
def setup(bot: commands.Bot):
    bot.add_cog(UserEmojis(bot))

import nextcord
from nextcord.ext import commands
import emoji
import re


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

    ######################################################################
    #   !addUserEmoji
    ######################################################################
    @commands.command(name="addUserEmoji")
    async def add_user_emoji(self, ctx, emoji: str):
        """
        Adds an emoji to all of your messages

        If you want to use a custom emoji from another server, Automoji MUST be in that server as well.

        * This is a SERVER-ONLY command.
        """
        # If 'arg' isn't an emoji, sends an error message.
        if not self.is_emoji(emoji):
            await ctx.send("Invalid argument. Are you sure that's an emoji?")
            return

        # Updates the row with the user's emoji.
        self.bot.cur.execute(
            "UPDATE emojis SET emoji=? WHERE guild=? AND user=?;",
            (emoji, ctx.guild.id, ctx.author.id),
        )

        self.bot.conn.commit()

        # Reacts to the user's message.
        await self.bot.bot_react(ctx.message)

    # No explicitly caught exceptions.
    @add_user_emoji.error
    async def add_user_emoji_error(self, ctx, error):
        if type(error) not in self.cog_errors:
            self.bot.logger.warning(error)

    ######################################################################
    #   !getUserEmoji
    ######################################################################
    @commands.command(name="getUserEmoji")
    async def get_user_emoji(self, ctx, member: nextcord.Member = None):
        """
        Gets a user's emoji

        * This is a SERVER-ONLY command.
        """
        # If the user doesn't specify a member, they default to being the member.
        if member == None:
            member = ctx.author

        # Gets the member's emoji.
        self.bot.cur.execute(
            "SELECT emoji FROM emojis WHERE guild=? AND user=?;",
            (ctx.guild.id, member.id),
        )

        if (emoji := self.bot.cur.fetchone()[0]) is None:
            await ctx.send(f"{member.name} doesn't have an emoji!")
        else:
            await ctx.send(f"{member.name}'s emoji is {emoji}!")

    # Explicitly caught exception: MemberNotFound
    @get_user_emoji.error
    async def get_user_emoji_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("I couldn't find that user...")
        elif type(error) not in self.cog_errors:
            self.bot.logger.warning(error)

    ######################################################################
    #   End commands
    ######################################################################

    # Determines if 'arg' is a valid emoji.
    # A valid emoji can be: (1) unicode, or (2) custom.
    def is_emoji(self, arg: str):
        # (1) Unicode emojis
        if emoji.emoji_count(arg) == 1:
            return True

        # (2) Custom emojis
        if bool(result := re.match("<a?:(\w+):(\d{18})>", arg)):
            id = int(result.group(2))
            return self.bot.get_emoji(id) is not None


# Required function for an extension.
def setup(bot: commands.Bot):
    bot.add_cog(UserEmojis(bot))

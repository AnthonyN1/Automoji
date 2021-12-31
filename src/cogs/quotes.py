import discord
from discord.ext import commands
import random

from am_logging import logger


class Quotes(commands.Cog):
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

    @commands.command(name="setQuoteChannel")
    async def set_quote_channel(self, ctx, channel: str):
        """
        Sets the channel that Automoji will look at for quotes.

        * This is a SERVER-ONLY command.
        """
        # If the guild isn't in the dictionaries yet, adds it.
        if ctx.guild not in self.bot.quotes_channels:
            self.bot.quotes_channels[ctx.guild] = None
        if ctx.guild not in self.bot.quotes:
            self.bot.quotes[ctx.guild] = list()

        # If the guild already has a quote channel, sends an error message.
        if self.bot.quotes_channels[ctx.guild] != None:
            await ctx.send(
                "The quote channel is already set! Try removing the channel."
            )
            return

        # Searches for the channel.
        quote_channel = None
        for c in ctx.guild.text_channels:
            if channel == c.name:
                if quote_channel != None:
                    await ctx.send(
                        "There are multiple channels with that name! Maybe rename one?"
                    )
                    return
                quote_channel = c

        # If the channel is not found, sends and error message.
        if quote_channel == None:
            await ctx.send(f"Sorry, {channel} is not a valid channel!")
            return

        # Gets all the quotes in the channel.
        quote_list = list()
        async for m in quote_channel.history():
            if m.author.id != self.bot.user.id:
                quote_list.append(m)
            else:
                logger.warning(f"Omitted: {m.clean_content} from quote list")

        self.bot.quotes_channels[ctx.guild] = quote_channel
        self.bot.quotes[ctx.guild] = quote_list

        await self.bot.bot_react(ctx.message)

    # No explicitly caught exceptions.
    @set_quote_channel.error
    async def set_quote_channel_error(self, ctx, error):
        if type(error) not in self.cog_errors:
            logger.warning(error)

    @commands.command(name="removeQuoteChannel")
    async def remove_quote_channel(self, ctx):
        """
        Frogets the channel that Automoji looks at for quotes.

        * This is a SERVER-ONLY command.
        """
        if (
            ctx.guild not in self.bot.quotes_channels
            or self.bot.quotes_channels[ctx.guild] == None
        ):
            await ctx.send("No quote channel to remove!")
            return

        self.bot.quotes_channels[ctx.guild] = None
        self.bot.quotes[ctx.guild].clear()
        await self.bot.bot_react(ctx.message)

    # No explicitly caught exceptions.
    @remove_quote_channel.error
    async def remove_quote_channel_error(self, ctx, error):
        if type(error) not in self.cog_errors:
            logger.warning(error)

    @commands.command(name="getQuote")
    async def get_quote(self, ctx):
        """
        Gets a random quote from the quote channel.

        * This is a SERVER-ONLY command.
        """
        if (
            ctx.guild not in self.bot.quotes_channels
            or self.bot.quotes_channels[ctx.guild] == None
        ):
            await ctx.send("No quote channel set!")
            return
        try:
            random_message = random.choice(self.bot.quotes[ctx.guild])
        except IndexError:
            await ctx.send("Quotes channel contains no valid quotes!")
            return

        # Sends a clean version of the message to the current channel.
        await ctx.send(random_message.clean_content)

    # No explicitly caught exceptions.
    @get_quote.error
    async def get_quote_error(self, ctx, error):
        if type(error) not in self.cog_errors:
            logger.warning(error)


# Required function for an extension.
def setup(bot: commands.Bot):
    bot.add_cog(Quotes(bot))

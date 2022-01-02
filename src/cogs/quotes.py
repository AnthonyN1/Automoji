from discord.ext import commands
import random

from am_logging import logger
from am_db import db_conn, db_cur


class Quotes(commands.Cog, command_attrs=dict(ignore_extra=False)):
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
    #   !setQuoteChannel
    ######################################################################
    @commands.command(name="setQuoteChannel")
    async def set_quote_channel(self, ctx, channel: str):
        """
        Sets the channel that Automoji will look at for quotes

        * This is a SERVER-ONLY command.
        """
        # Checks if the channel is already set.
        db_cur.execute(
            "SELECT COUNT(ROWID) FROM quote_channels WHERE guild=? AND channel IS NOT NULL;",
            (ctx.guild.id,),
        )
        if db_cur.fetchone()[0] == 1:
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

        # If the channel is not found, sends an error message.
        # Else, updates the row in the table.
        if quote_channel == None:
            await ctx.send(f"Invalid argument. Are you sure that's a channel?")
            return
        else:
            db_cur.execute(
                "UPDATE quote_channels SET channel=? WHERE guild=?;",
                (quote_channel.id, ctx.guild.id),
            )

        # Gets all the quotes in the channel.
        async for m in quote_channel.history():
            if m.author.id != self.bot.user.id:
                db_cur.execute(
                    "INSERT INTO quotes VALUES (?, ?)", (ctx.guild.id, m.clean_content)
                )
            else:
                logger.warning(f"Omitted: {m.clean_content} from quote list")

        db_conn.commit()

        await self.bot.bot_react(ctx.message)

    # No explicitly caught exceptions.
    @set_quote_channel.error
    async def set_quote_channel_error(self, ctx, error):
        if type(error) not in self.cog_errors:
            logger.warning(error)

    ######################################################################
    #   !removeQuoteChannel
    ######################################################################
    @commands.command(name="removeQuoteChannel")
    async def remove_quote_channel(self, ctx):
        """
        Forgets the channel that Automoji looks at for quotes

        * This is a SERVER-ONLY command.
        """
        # Checks if the channel isn't set.
        # If it isn't sends an error message.
        db_cur.execute(
            "SELECT COUNT(ROWID) FROM quote_channels WHERE guild=? AND channel IS NULL;",
            (ctx.guild.id,),
        )
        if db_cur.fetchone()[0] == 1:
            await ctx.send("No quote channel to remove!")
            return

        # Removes the channel and all quotes.
        db_cur.execute(
            "UPDATE quote_channels SET channel=NULL WHERE guild=?;", (ctx.guild.id,)
        )
        db_cur.execute("DELETE FROM quotes WHERE guild=?", (ctx.guild.id,))

        db_conn.commit()

        await self.bot.bot_react(ctx.message)

    # No explicitly caught exceptions.
    @remove_quote_channel.error
    async def remove_quote_channel_error(self, ctx, error):
        if type(error) not in self.cog_errors:
            logger.warning(error)

    ######################################################################
    #   !getQuote
    ######################################################################
    @commands.command(name="getQuote")
    async def get_quote(self, ctx):
        """
        Gets a random quote from the quote channel

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

    ######################################################################
    #   End commands
    ######################################################################


# Required function for an extension.
def setup(bot: commands.Bot):
    bot.add_cog(Quotes(bot))

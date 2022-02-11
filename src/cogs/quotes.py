from nextcord.ext import commands


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
        if quote_channel == None:
            await ctx.send(f"Invalid argument. Are you sure that's a channel?")
            return

        # Updates the row in the table.
        self.bot.cur.execute(
            "UPDATE quote_channels SET channel=? WHERE guild=?;",
            (quote_channel.id, ctx.guild.id),
        )

        # Deletes the previous quotes from the table.
        self.bot.cur.execute("DELETE FROM quotes WHERE guild=?", (ctx.guild.id,))

        # Gets all the quotes in the channel.
        async for m in quote_channel.history():
            if m.author.id != self.bot.user.id:
                self.bot.cur.execute(
                    "INSERT INTO quotes VALUES (?, ?)", (ctx.guild.id, m.clean_content)
                )
            else:
                self.bot.logger.warning(f"Omitted: {m.clean_content} from quote list")

        self.bot.conn.commit()

        await self.bot.bot_react(ctx.message)

    # No explicitly caught exceptions.
    @set_quote_channel.error
    async def set_quote_channel_error(self, ctx, error):
        if type(error) not in self.cog_errors:
            self.bot.logger.warning(error)

    ######################################################################
    #   !getQuote
    ######################################################################
    @commands.command(name="getQuote")
    async def get_quote(self, ctx):
        """
        Gets a random quote from the quote channel

        * This is a SERVER-ONLY command.
        """
        # Sends an error message if the channel isn't set.
        self.bot.cur.execute(
            "SELECT channel FROM quote_channels WHERE guild=?;", (ctx.guild.id,)
        )
        if self.bot.cur.fetchone()[0] is None:
            await ctx.send("No quote channel set!")
            return

        # Sends an error message if there are no quotes.
        self.bot.cur.execute(
            "SELECT COUNT(ROWID) FROM quotes WHERE guild=?;", (ctx.guild.id,)
        )
        if self.bot.cur.fetchone()[0] == 0:
            await ctx.send("Quotes channel contains no valid quotes!")
            return

        # Sends a random quote.
        self.bot.cur.execute(
            "SELECT quote FROM quotes WHERE guild=? ORDER BY RANDOM() LIMIT 1;",
            (ctx.guild.id,),
        )
        await ctx.send(self.bot.cur.fetchone()[0])

    # No explicitly caught exceptions.
    @get_quote.error
    async def get_quote_error(self, ctx, error):
        if type(error) not in self.cog_errors:
            self.bot.logger.warning(error)

    ######################################################################
    #   End commands
    ######################################################################


# Required function for an extension.
def setup(bot: commands.Bot):
    bot.add_cog(Quotes(bot))

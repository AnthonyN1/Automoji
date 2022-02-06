import nextcord
from nextcord.ext import commands


class Automoji(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = kwargs["logger"]
        self.conn = kwargs["conn"]
        self.cur = kwargs["cur"]

        self.robot_emoji = "\U0001F916"
        self.question_emoji = "\U00002753"

    ######################################################################
    #   Overridden commands
    ######################################################################
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(
                "I couldn't recognize that command. Please see '!help' for a list of commands."
            )

    async def on_guild_join(self, guild: nextcord.Guild):
        # Inserts the guild ID into the quote table.
        self.cur.execute("INSERT INTO quote_channels VALUES (?, NULL);", (guild.id,))

        # Inserts the guild ID and user IDs into the emojis table.
        for m in guild.members:
            if not m.bot:
                self.cur.execute(
                    "INSERT INTO emojis VALUES (?, ?, NULL);", (guild.id, m.id)
                )

        self.conn.commit()

    async def on_guild_remove(self, guild: nextcord.Guild):
        # Deletes the row containing the guild ID from the quote table.
        self.cur.execute("DELETE FROM quote_channels WHERE guild=?;", (guild.id,))

        # Deletes rows contains the guild ID from the emojis table.
        self.cur.execute("DELETE FROM emojis WHERE guild=?;", (guild.id,))

        self.conn.commit()

    async def on_member_join(self, member: nextcord.Member):
        # Inserts the member ID into the emojis table.
        if not member.bot:
            self.cur.execute(
                "INSERT INTO emojis VALUES (?, ?, NULL);", (member.guild.id, member.id)
            )

        self.conn.commit()

    async def on_member_remove(self, member: nextcord.Member):
        # Deletes the row containing the member ID from the emojis table.
        if not member.bot:
            self.cur.execute(
                "DELETE FROM emojis WHERE guild=? AND user=?;",
                (member.guild.id, member.id),
            )

        self.conn.commit()

    async def on_message(self, message: nextcord.Message):
        # Avoids the bot recursing through its own messages.
        if message.author.id == self.user.id or message.author.bot:
            return

        # Reacts to the user's message with their emoji.
        await self.react_user_emoji(message)

        await self.process_commands(message)

    async def on_ready(self):
        print("Automoji is now online!")

    ######################################################################
    #   End overridden commands
    ######################################################################

    # Reacts to a message using the robot emoji.
    async def bot_react(self, message: nextcord.Message):
        try:
            await message.add_reaction(self.robot_emoji)
        except nextcord.DiscordException as e:
            self.logger.warning(e)

    # Reacts to a message using the question mark emoji.
    async def invalid_react(self, message: nextcord.Message):
        try:
            await message.add_reaction(self.question_emoji)
        except nextcord.DiscordException as e:
            self.logger.warning(e)

    # Reacts to a user's message with their emoji.
    async def react_user_emoji(self, message: nextcord.Message):
        # Gets the user's emoji.
        self.cur.execute(
            "SELECT emoji FROM emojis WHERE guild=? AND user=?;",
            (message.guild.id, message.author.id),
        )
        em = self.cur.fetchone()[0]

        if em is not None:
            # Reacts to the user's message with their emoji.
            try:
                await message.add_reaction(em)
            except nextcord.DiscordException as e:
                self.logger.warning(e)

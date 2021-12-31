import discord
from discord.ext import commands
import emoji

from am_logging import logger


class Automoji(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Constructs a dictionary, where the keys are Guilds, and the values are dictionaries.
        # In the sub-dictionaries, the keys are Members, and the values are strings that represent emojis.
        self.user_emojis = {}

        self.robot_emoji = "\U0001F916"

        # Constructs dictionaries, where the keys and Guilds, and the values are Channels and lists, respectively.
        self.quotes_channels = {}
        self.quotes = {}

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(
                "I couldn't recognize that command. Please see '!help' for a list of commands."
            )

    async def on_message(self, message: discord.Message):
        # Avoids the bot recursing through its own messages.
        if message.author.id == self.user.id:
            return

        # Adds a quote if sent in the quotes channel
        if message.channel == self.quotes_channels[message.guild]:
            self.add_quote(message)
        
        # Reacts to the user's message with their emoji.
        await self.react_user_emoji(message)

        await self.process_commands(message)

    async def on_ready(self):
        print("Automoji is now online!")

    # Reacts to a message using the robot emoji.
    async def bot_react(self, message: discord.Message):
        try:
            await message.add_reaction(self.robot_emoji)
        except discord.DiscordException as e:
            logger.warning(e)

    # Reacts to a user's message with their emoji.
    async def react_user_emoji(self, message: discord.Message):
        try:
            # Gets the user's emoji.
            user = message.author
            em = self.user_emojis[message.guild][user]
        except KeyError:
            # If the user doesn't have an emoji, don't do anything.
            return

        # Reacts to the user's message with their emoji.
        try:
            await message.add_reaction(em)
        except discord.DiscordException as e:
            logger.warning(e)

    # Determines if 'arg' is a valid emoji.
    # A valid emoji can be: (1) unicode, or (2) custom to the current guild.
    def is_emoji(self, guild: discord.Guild, arg: str):
        # (1) Unicode emojis
        if emoji.emoji_count(arg) == 1:
            return True

        # (2) Custom emojis in the current guild
        if (guild != None) and (any(arg == str(em) for em in guild.emojis)):
            return True

        return False

    # Adds a quote to quote list if valid
    def add_quote(self, message: discord.Message):
        # Checks if guild is in dictionary
        if message.guild not in self.quotesChannels or message.guild not in self.quotes:
            return

        # Checks if quotesChannel is called and if quotes Channel is the message's channel
        if (
            self.quotesChannels[message.guild] == None
            or message.channel != self.quotesChannels[message.guild]
        ):
            return

        # Checks if the message is a valid quote
        if message.author.id != self.user.id:
            self.quotes[message.guild].append(message)
        else:
            print(f"Omitted: {message.clean_content} from quote list")
            return

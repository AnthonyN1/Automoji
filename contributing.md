# Contributing to Automoji
## Preface
Want to contribute to Automoji? Great! You're more than welcome to submit a Pull Request with a new feature, or a bug-fix. Please make sure to skim all the Python files (and in particular: ```automoji.py``` and ```cogs/user_emojis.py```) to get a sense of the code style before submiting a Pull Request.

Additionally, please familiarize yourself (if you aren't already) with the [documentation](https://discordpy.readthedocs.io/en/stable/) for ```discord.py```, the API that Automoji is built off of.

## About ```discord.py```
Automoji makes heavy use of the API extension ```discord.ext.commands```, so some familiarity is required. As is probably evident, all Python files in the ```cogs``` directory are classes that subclass ```Cog```. These classes are loaded into the ```Bot``` as an extension (see ```main.py``` for more detail).

As such, please faithfully conform to the syntax and conventions laid out in the Python standard, as well as in the ```discord.py``` documentation. See the files in the ```cogs``` directory for an idea of the project's code styling.

## Styling your Cog
* ```import``` statements go on the first couple lines of any Python file, and are sorted alphabetically by the library name.
* Two (2) newlines separate ```import``` statements and the class declaration.
* All classes should subclass ```commands.Cog```. The ```name``` attribute should be human-readable, and (unless explicitly necessary) ```ignore_extra``` should be set to ```False```.
* Follow ```user_emojis.py``` for an example of an ```__init__``` function. ```cog_errors``` should be a list of the exceptions that all commands in the Cog handle in a similar fashion.
* ```cog_check``` and ```cog_command_error``` are optional, but should be present most of the time. See the comments in ```user_emojis.py``` for more information.
* Two (2) newlines separate ```__init__```, ```cog_check``` and ```cog_command_error```, and any new commands. For all other cases, one (1) newline is used.
* For new commands, the ```name``` attribute should be camel-cased, while the function should be snake-cased.
* Try to use function annotations for function parameters as much as possible, except for the ```self``` parameter.
* Construct a docstring for command functions, since these get shown through the ```!help``` command. See ```user_emojis.py``` for examples.
* Be smart with commenting your code. Don't over-do it, but at least include a comment for an independent code chunk.
* For any command that doesn't respond to a user, add ```await self.bot.bot_react(ctx.message)``` to the end of the function. This makes Automoji react to the command message with :robot:.
* An exception handler must be present for every command added, even if the handler doesn't catch any specific exception. This code segment should be present in all exception handlers:
```
elif type(error) not in self.cog_errors:
	print(f"Caught unexpected exception at <function>: {type(error)}")
```
* At the end of the file (separated by two (2) newlines) should be the ```setup``` function, which is required for all extensions. See ```user_emojis.py``` for an example.
* At the end of all Python files should be a newline.

## Additional notes
* If your Cog imports a Python library, please include it in ```requirements.txt``` if it isn't already there.
* As stated in ```runtime.txt```, Automoji is built using Python 3.8.5. So, do not use any Python syntax that isn't supported in version 3.8.5.
* When adding a Cog, be sure to modify the ```extensions``` list in ```main.py``` so that the Cog is actually loaded in.
* If it isn't already apparent, Automoji handles errors using exceptions. Thus, make heavy use of exceptions. Plan for the worst!
* If you notice any other code styling point that's missing here, feel free to modify this file to include it!

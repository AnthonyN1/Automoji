# Automoji 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## About
Automoji is an open-source Discord bot that's in its early stages of development! Automoji will come with a variety of commands that Discord users can use, either in DMs or in a server. To invite Automoji to your Discord server, click on [this](https://discord.com/api/oauth2/authorize?client_id=764554242362441738&permissions=137439341632&scope=bot) link!

If you find this project cool/interesting/exciting, please leave a :star: on this repository! We would greatly appreciate it.

## Features
* ```User emojis```: personalize your messages with an emoji of your choice
* ...and more soon to come!

## Usage (link)
You can get Automoji on your server through [this](https://discord.com/api/oauth2/authorize?client_id=764554242362441738&permissions=137439341632&scope=bot) link!

If you choose to deny Automoji some or all permissions, please note that certain commands will not behave as expected.

## Usage (self-hosted)
If you wish to host Automoji on your own machine (or using a cloud service), you can clone this repository:
```
git clone https://github.com/AnthonyN1/Automoji.git
```
Automoji uses Python 3.8.10. See ```requirements.txt``` for a list of Python dependencies Automoji uses.

Visit the [Discord Developer Portal](https://discord.com/developers/applications) to create an application and bot. Use the bot's token to set an environment variable named ```TOKEN```. Additionally, Automoji requires you to enable the Server Members Intent, under Privileged Gateway Intents. The required bot permissions are:

* Read Messages/View Channels
* Send Messages
* Manage Messages
* Embed Links
* Attach Files
* Read Message History
* Use External Emojis
* Use External Stickers
* Add Reactions

Once everything is set up, simply run ```python3 main.py``` or equivalent in your terminal.

## Contributing
Have an idea for a feature that you want to see implemented? Find a bug in the pre-existing code? You're more than welcome to submit a Pull Request! See ```contributing.md``` for a full guide on contributing.

## License
Released under the [MIT License](https://opensource.org/licenses/MIT).

## Major Contributors
* [AnthonyN1](https://github.com/AnthonyN1) on GitHub.

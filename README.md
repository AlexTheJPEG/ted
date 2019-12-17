# Ted
Just another Discord bot made with Python.

# Dependencies
There's a Pipfile in this repository, so if you have Pipenv or a similar packaging tool, you should be able to install the dependencies automatically.

# Setup
Create a new file in the current directory named `settings.json`. This will contain all your settings for the bot.

It should look something like this:
```
{
  "token": "insert token here",
  "prefix": "$",
  "respond_to_self": "False",
  "respond_to_bots": "False"
}
```
`token` - Your bot's token

`prefix` - What character(s) should be used before commands

`respond_to_self` - Should the bot be able to respond to itself? (False is recommended)

`respond_to_bots` - Should the bot be able to respond to other bots? (False is recommended)

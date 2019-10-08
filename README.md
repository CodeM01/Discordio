# Discordio

A discord bot library, whether you’re making your own !wumpus commands or looking to Log In With Discord, we’ve got you covered.

What will the code look like?...

```python

from bot import client as Cli

Client = Cli.Client("bot_token_here")

# This code will return a list of dictionaries, each one representing a channel

@Client.async_handler                               
async def message_received(message):                              
    print(message.guild.get_channels())                           


Client.run()                 
```

# Discordio

A discord bot library, whether you’re making your own !wumpus commands or looking to Log In With Discord, we’ve got you covered.

Below is an example of code which will print out the contents of a message when a message is sent...

```python

from RawDiscordBot import Client as Cli

Client = Cli.Client("bot_token_here")

# This code will print the id of the author of the message

@Client.async_handler                               
async def message_received(message):                              
    print(message.author)                              


Client.run()                 
```

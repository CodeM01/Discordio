# Discordio

A work in progress discord bot library...

```python

from client import Client

bot_client = Client("my_token")

@bot_client.async_handler
async def message_create(message):
    if message.content == "hi":
        print(await message.guild.get_channels())
    else:
        print(message.channel.name)

bot_client.run()
              
```

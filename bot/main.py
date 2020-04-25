# Example Code
from client import Client

Client = Client("NjA4Nzc0MzIzMTkyNDYzMzcx.Xb3nJg.4WKrFTKK0oKCWoZEgxiD9FWHQak")

@Client.async_handler
async def message_create(message):
    channels = await message.guild.get_channels()
    print(channels)

Client.run()

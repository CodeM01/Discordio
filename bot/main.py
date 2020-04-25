from client import Client

Client = Client(<bot_id>)

@Client.async_handler
async def message_create(message):
    channels = await message.guild.get_channels()
    print(channels)

Client.run()


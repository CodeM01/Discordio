import asyncio

from json_management import json_creator
from channel_class import Channel
from guild_class import Guild

class message:

    def __init__(self, user, message_dict):
        self.author_id = message_dict["d"]["author"]["id"]
        self.content = message_dict["d"]["content"]
        self.guild_id = message_dict["d"]["guild_id"]
        self.guild = Guild(user, self.guild_id)
        self.channel_id = message_dict["d"]["channel_id"]
        self.channel = Channel(user, self.channel_id)


async def heartbeat(user):
    attempts = 0
    while True:
        if user.gateway_data["hello"]:

            if attempts < 2:
                if not user.gateway_data["heartbeat_ack"]:
                    attempts += 1
                else:
                    user.gateway_data["heartbeat_ack"] = False
                    attempts = 1

                await user.ws.send(await json_creator.create_heartbeat(user.gateway_data["s"]))
                await asyncio.sleep(user.gateway_data["heartbeat_interval"])
            else:
                await user.ws.close()


async def message_create(user, loaded_dictionary):
    message_obj = message(user, loaded_dictionary)

    channel_data = await message_obj.channel.get_channel_data()
    message_obj.channel.topic = channel_data["topic"]
    message_obj.channel.name = channel_data["name"]

    if user.functions.get("message_create"):
        function = user.functions["message_create"]
        await function(message_obj)


async def ready(user, loaded_dictionary):
    user.bot_data["user"] = loaded_dictionary["d"]["user"]


async def guild_create(user, loaded_dictionary):
    pass

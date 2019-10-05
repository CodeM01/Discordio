import asyncio

from bot.json import json_creator as Creator
from bot.entities.channel.channel_class import Channel
from bot.entities.guild import load_guild


class message:

    def __init__(self, user, message_dict):
        self.author_id = message_dict["d"]["author"]["id"]
        self.content = message_dict["d"]["content"]
        self.guild_id = message_dict["d"]["guild_id"]
        self.channel = Channel(user, self.guild_id, message_dict["d"]["channel_id"] )


async def heartbeat(user):
    attempts = 0
    while True:
        if user.states["op_code_10"]:
            if attempts < 2:

                if not user.states["op_code_11"]:
                    attempts += 1
                else:
                    user.states["op_code_11"] = False
                    attempts = 1

                await user.ws.send(await Creator.create_heartbeat(user.s))
                await asyncio.sleep(user.heartbeat_interval)
            else:
                await user.ws.close()


# Separate functions for each event (for organisation)
async def message_create(user, obj):

    message_obj = message(user, obj)

    if user.functions.get("message_received"):
        function = user.functions["message_received"]
        await function(message_obj)


async def ready(user, obj):
    # Load guilds
    guilds = obj["d"]["guilds"]
    await load_guild.load_guilds(user, guilds)

    # Load User Data
    user.user = obj["d"]["user"]


async def guild_create(user, obj):
    guild = obj["d"]

    await load_guild.load_guilds(user, [guild])
    await load_guild.load_guild_data(user, guild)

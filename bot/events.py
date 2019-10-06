import asyncio

from bot.json import JsonCreator as Creator
from bot.entities.channel.channel_class import Channel
from bot.entities.guild import loading_guild

class message:

    def __init__(self, user, message_dict):
        self.author_id = message_dict["d"]["author"]["id"]
        self.content = message_dict["d"]["content"]
        self.guild_id = message_dict["d"]["guild_id"]
        self.channel = Channel(user, self.guild_id, message_dict["d"]["channel_id"])


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

                await user.ws.send(await Creator.create_heartbeat(user.gateway_data["s"]))
                await asyncio.sleep(user.gateway_data["heartbeat_interval"])
            else:
                await user.ws.close()


# Separate functions for each event (for organisation)
async def message_create(user):

    message_obj = message(user, user.loaded_dictionary)

    if user.functions.get("message_received"):
        function = user.functions["message_received"]
        await function(message_obj)


async def ready(user):
    # Load guilds
    guilds = user.loaded_dictionary["d"]["guilds"]
    await loading_guild.load_guilds(user, guilds)

    print(user.loaded_dictionary, user)

    # Load User Data
    user.bot_data["user"] = user.loaded_dictionary["d"]["user"]


async def guild_create(user):
    guild = user.loaded_dictionary["d"]

    await loading_guild.load_guilds(user, [guild])
    await loading_guild.load_guild_data(user, guild)

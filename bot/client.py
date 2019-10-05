import websockets
import json
import asyncio

from bot.json import json_creator as Creator
from bot.events import events


class Client:

    gateway_link = "wss://gateway.discord.gg/"

    def __init__(self, bot_token):
        self.functions = {}
        self.bot_token = bot_token
        self.s = None
        self.ws = None
        self.session_id = None
        self.heartbeat_interval = None
        self.guilds = {}
        self.user = None
        self.states = {"initiated": False, "op_code_11": False, "op_code_10": False}

    """ 
    Seperate to __init__ so that the built-in functions aren't blocked
    by the client; we need to get all of the in-built functions before we start heartbeating
    and carrying out all of the other tasks as the client takes the main thread.
    """

    def run(self):
        self.async_handler(self.web_socket)

    async def web_socket(self):
        async with websockets.connect(Client.gateway_link) as ws:
            self.ws = ws
            while True:
                try:
                    response = await ws.recv()
                except websockets.ConnectionClosed as e:
                    print(e)
                    self.states["op_code_10"] = False
                    self.states["op_code_11"] = False
                    break

                loaded_dictionary = json.loads(response)
                op = loaded_dictionary["op"]
                self.s = loaded_dictionary["s"]

                print(response)

                # Sent in as python dictionary
                if op == 10:
                    self.states["op_code_10"] = True
                    self.heartbeat_interval = loaded_dictionary["d"]["heartbeat_interval"] / 1000
                    self.async_handler( Events.heartbeat )
                elif op == 11 and self.states["op_code_10"]:
                    if not self.states["initiated"]:
                        self.states["initiated"] = True
                        identify = await Creator.create_identify(self)
                        await asyncio.sleep(1)
                        await self.ws.send(identify)

                    self.states["op_code_11"] = True
                elif op == 0:
                    if loaded_dictionary["t"] == "READY":
                        asyncio.get_event_loop().create_task(Events.ready(self, loaded_dictionary))
                    elif loaded_dictionary["t"] == "MESSAGE_CREATE":
                        asyncio.get_event_loop().create_task(Events.message_create( self, loaded_dictionary))
                    elif loaded_dictionary["t"] == "GUILD_CREATE":
                        asyncio.get_event_loop().create_task(Events.guild_create(self, loaded_dictionary))

    def async_handler(self, function, *args):

        # Put them here just in case I need to use them in the future
        current_functions = ["message_received"]

        if function.__name__ == "web_socket":
            task = asyncio.get_event_loop().create_task(function())
            asyncio.get_event_loop().run_until_complete(task)
        elif function.__name__ == "heartbeat":
            asyncio.get_event_loop().create_task(Events.heartbeat(self))
        elif function.__name__ == "GUILD_CREATE":
            asyncio.get_event_loop().create_task(Events.guild_create(self, args))
        elif function.__name__ == "READY":
            pass

        # Built-in functions

        if function.__name__ in current_functions:
            if not self.functions.get("message_received"):
                self.functions["message_received"] = function

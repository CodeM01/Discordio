import websockets
import json
import asyncio

from bot.json import json_creator as Creator
from bot import events


class Client:
    gateway_link = "wss://gateway.discord.gg/"

    def __init__(self, bot_token):
        self.states = {"initiated": False, "op_code_11": False, "op_code_10": False}
        self.gateway_data = {"s": None, "session_id": None, "heartbeat_interval": None}
        self.bot_data = {"token": bot_token}
        self.functions = dict ()

        self.ws = None
        self.guilds = {}

    """ 
    Run the client seperately so that all of the in-built functions aren't blocked
    by the client; we need to get all of the in-built functions before we start heartbeating
    and carrying out all of the other tasks as the client takes the main thread.
    """

    def run(self):
        task = asyncio.get_event_loop().create_task(self.web_socket())
        asyncio.get_event_loop().run_until_complete(task)

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
                self.gateway_data["s"] = loaded_dictionary["s"]

                print(response)

                if op == 10:
                    self.states["op_code_10"] = True
                    self.gateway_data["heartbeat_interval"] = loaded_dictionary["d"]["heartbeat_interval"] / 1000
                    self.add_task(Events.heartbeat(self))

                elif op == 11 and self.states["op_code_10"]:
                    if not self.states["initiated"]:
                        self.states["initiated"] = True
                        identify = await Creator.create_identify(self)
                        await asyncio.sleep(1)
                        await self.ws.send(identify)
                    self.states["op_code_11"] = True

                if loaded_dictionary["t"] == "READY":
                    self.add_task(Events.ready(self, loaded_dictionary))
                elif loaded_dictionary["t"] == "MESSAGE_CREATE":
                    self.add_task(Events.message_create(self, loaded_dictionary))
                elif loaded_dictionary["t"] == "GUILD_CREATE":
                    self.add_task(Events.guild_create(self, loaded_dictionary))

    @staticmethod
    def add_task(task):
        asyncio.get_event_loop().create_task(task)

    def async_handler(self, function):
        current_functions = ["message_received"]

        # Checking to see if the function that was inputted is a valid event function

        if function.__name__ in current_functions:
            if not self.functions.get("message_received"):
                self.functions["message_received"] = function

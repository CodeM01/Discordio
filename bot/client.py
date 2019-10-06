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
        self.events = {"READY": Events.ready, "MESSAGE_CREATE": Events.message_create,
                       "GUILD_CREATE": Events.guild_create}
        self.bot_data = {"token": bot_token}
        self.functions = {}

        # WebSocket
        self.ws = None
        # Guilds bot is in
        self.guilds = {}

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

                input_event = loaded_dictionary["t"]

                if input_event:
                    for event in self.events:
                        if event == input_event:
                            await self.events[input_event](self, loaded_dictionary)
                else:
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

    @staticmethod
    def add_task(task):
        asyncio.get_event_loop().create_task(task)

    def async_handler(self, function):
        current_functions = ["message_received"]

        # Checking to see if the function that was inputted is a valid event function

        if function.__name__ in current_functions:
            if not self.functions.get("message_received"):
                self.functions["message_received"] = function

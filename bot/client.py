import websockets
import json
import asyncio

from RawDiscordBot.json import JsonCreator as Creator
from RawDiscordBot import Events


class Client:
    gateway_link = "wss://gateway.discord.gg/"

    def __init__(self, bot_token):
        self.states = {"initiated": False, "op_code_11": False, "op_code_10": False}
        self.gateway_data = {"s": None, "session_id": None, "heartbeat_interval": None}
        self.event_functions = {"READY": Events.ready, "MESSAGE_CREATE": Events.message_create,
                                "GUILD_CREATE": Events.guild_create}
        self.op_code_event_functions = {10: self.op_10, 11: self.op_11}
        self.bot_data = {"token": bot_token}
        self.functions = {}
        self.loaded_dictionary = {}

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

                self.loaded_dictionary = json.loads(response)
                input_event = self.loaded_dictionary["t"]
                input_op = self.loaded_dictionary["op"]
                self.gateway_data["s"] = self.loaded_dictionary["s"]

                print(response)

                if input_event and input_event in self.event_functions:
                    for event in self.event_functions.keys():
                        if event == input_event:
                            await self.event_functions[input_event](self)

                elif input_op:
                    for op in self.op_code_event_functions.keys():
                        if op == input_op:
                            await self.op_code_event_functions[op]()

    @staticmethod
    def add_task(task):
        asyncio.get_event_loop().create_task(task)

    async def op_10(self):
        self.states["op_code_10"] = True
        self.gateway_data["heartbeat_interval"] = self.loaded_dictionary["d"]["heartbeat_interval"] / 1000
        self.add_task(Events.heartbeat(self))

    async def op_11(self):
        if not self.states["initiated"]:
            self.states["initiated"] = True
            identify = await Creator.create_identify(self)
            await asyncio.sleep(1)
            await self.ws.send(identify)
        self.states["op_code_11"] = True


    def async_handler(self, function):
        current_functions = ["message_received"]

        # Checking to see if the function that was inputted is a valid event function

        if function.__name__ in current_functions:
            if not self.functions.get("message_received"):
                self.functions["message_received"] = function

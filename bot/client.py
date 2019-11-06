import websockets
import json
import asyncio

from json_management import json_creator as creator
from asynchronous_http import aiohttp_session
import events


class Client:
    gateway_link = "wss://gateway.discord.gg/"

    def __init__(self, bot_token):
        self.gateway_data = {"s": None, "session_id": None, "heartbeat_interval": None,
                            "operating": False, "heartbeat_ack": False, "hello": False}
        self.gateway_events = {"READY": events.ready, "MESSAGE_CREATE": events.message_create,
                              "GUILD_CREATE": events.guild_create}
        self.bot_data = {"token": bot_token}
        self.functions = {}
        self.loop = asyncio.get_event_loop()
        self.aiohttp_client_session = aiohttp_session(self)

        """"WebSocket"""
        self.ws = None

    def run(self):
        self.loop.run_until_complete(self.web_socket())

    async def web_socket(self):
        async with websockets.connect(Client.gateway_link) as ws:
            self.ws = ws
            while True:
                try:
                    response = await ws.recv()
                except websockets.ConnectionClosed as e:
                    self.gateway_data["hello"] = False
                    self.gateway_data["heartbeat_ack"] = False
                    break

                loaded_dictionary = json.loads(response)
                op = loaded_dictionary["op"]
                self.loaded_dictionary = loaded_dictionary
                self.gateway_data["s"] = loaded_dictionary["s"]

                print(response.encode("utf-8"))

                if op == 10:
                    self.gateway_data["hello"] = True
                    self.gateway_data["heartbeat_interval"] = loaded_dictionary["d"]["heartbeat_interval"] / 1000
                    self.add_task(events.heartbeat(self))

                elif op == 11:
                    if not self.gateway_data["operating"]:
                        self.gateway_data["operating"] = True
                        identify = await creator.create_identify(self)
                        await self.ws.send(identify)
                    self.gateway_data["heartbeat_ack"] = True

                event = self.gateway_events.get(loaded_dictionary["t"])

                if self.gateway_events.get(loaded_dictionary["t"]):
                    self.add_task(event(self, loaded_dictionary))

    def add_task(self, task):
        self.loop.create_task(task)


    def async_handler(self, function):

        if function.__name__.upper() in self.gateway_events:
            if not self.functions.get(function.__name__):
                self.functions[function.__name__] = function
            else:
                raise("Two Or More Of The Same Built-in Function, Is Not Permitted")
        else:
            raise("Unrecognised Built-in Function")


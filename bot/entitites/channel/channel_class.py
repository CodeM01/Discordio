from http_request import http_request
import asyncio

class Channel:

    def __init__(self, user, channel_id):
        self.channel_id = channel_id
        self.user = user

    async def get_channel_data(self):
        load = {"request_type": "GET",
                "end_point": "/channels/" + self.channel_id,
                "headers": {"Authorization": "Bot " + self.user.bot_data["token"]}}

        return await self.user.aiohttp_client_session.http_request(load)

    async def send(self):
        response = http_request("channels/" + self.channel_id + "/messages", "POST", self.user.bot_data["token"])

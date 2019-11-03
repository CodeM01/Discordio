import aiohttp
import asyncio
import json

class aiohttp_session():

    def __init__(self, user):
        self.user = user
        user.loop.create_task(self.create_session())

    async def create_session(self):
        self.session = aiohttp.ClientSession()
        self.requests = {"GET": self.get}
        self.request_error_codes = {"404: Not Found": "invalid url - invalid end_point",
                                    "401: Unauthorized": "unauthorized access to end_point"}

    async def http_request(self, load):

        if (load.get("end_point") and load.get("headers") and load.get("request_type")) is None:
            raise KeyError("end_point, headers or request_type not Specified in load")

        if not self.requests.get(load.get("request_type")):
            raise KeyError("invalid request_type")

        response = await self.requests[load.get("request_type")](load)
        return response



    async def get(self, load):
        url = "https://discordapp.com/api/v6/" + load.get("end_point")

        async with self.session.get(url, headers=load.get("headers")) as session:
            response = await session.text()

            if isinstance(response, str):
                try:
                    response = json.loads(response)
                except Exception as e: print(e)

                if isinstance(response, dict):
                    message = response.get("message")
                    if message:
                        raise Exception(self.request_error_codes.get(message))

            return response

import aiohttp
import asyncio
import json

class aiohttp_session():

    def __init__(self, user):
        self.user = user
        user.loop.create_task(self.create_session())


    async def create_session(self):
        self.session = aiohttp.ClientSession()
        self.requests = {"GET": self.get, "POST": self.post}
        self.request_error_codes = {"404: Not Found": "Invalid End_point",
                                    "401: Unauthorized": "Invalid Authorization Header"}


    async def http_request(self, load):

        if (load.get("end_point") and load.get("headers/data") and load.get("request_type")) is None:
            raise KeyError("End_point, headers/data or Request_type Not Specified In Load")

        if not self.requests.get(load.get("request_type")):
            raise KeyError("Invalid Request_type")

        return await self.requests[load.get("request_type")](load)

    async def get(self, load):
        url = "https://discordapp.com/api/v6/" + load.get("end_point")

        async with self.session.get(url, headers=load.get("headers/data")) as session:
            response = await session.text()
            loaded_response = await self.load_response(response)
            error = await self.check_for_error(response)

            if not error:
                return loaded_response


    async def post(self, load):

        """In Progress"""
        
        url = "https://discordapp.com/api/v6/" + load.get("end_point")

        try:
            json_dump = json.dumps(load.get("headers/data"))
        except ValueError:
            raise ValueError("The Load Could Not Be Dumped As Json")

        async with self.session.post(url=url, json=json_dump) as session:
            response = await session.text()
            loaded_response = await self.load_response(response)
            error = await self.check_for_error(loaded_response)

            if not error:
                return loaded_response


    async def check_for_error(self, response):
        if isinstance(response, dict):
            message = response.get("message")
            if message:
                raise Exception(self.request_error_codes.get(message))
                return True
            return False


    async def load_response(self, response):
        if isinstance(response, str):
            try:
                response = json.loads(response)
            except Exception: pass

            return response

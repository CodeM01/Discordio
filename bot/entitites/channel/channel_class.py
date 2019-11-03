import asyncio

class Channel:

    def __init__(self, user, channel_id):
        self.channel_id = channel_id
        self.user = user

        """ Getting all of the channel data """

        load = {"request_type": "GET",
                    "end_point": "/channels/609858340876451947",
                    "headers": {"Authorization": "Bot " + user.bot_data["token"]}}

        response = asyncio.get_event_loop().run_until_complete(user.aiohttp_client_session.http_request(load))
        #http_request("channels/" + self.channel_id, "GET", user.bot_data["token"])

        #self.name = response["name"]
        #self.topic = response["topic"]
        print(response)

    async def send(self):
        response = http_request("channels/" + self.channel_id + "/messages", "POST", self.user.bot_data["token"])

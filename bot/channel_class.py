import json_and_dictionary_constructor

class Channel:

    def __init__(self, user, channel_id):
        self.channel_id = channel_id
        self.user = user

    async def send(self, message):
        http_template = dictionary_templates.http_load
        message_template = dictionary_templates.new_message

        message_template["content"] = message
        message_template["tts"] = False

        http_template["request_type"] = "POST"
        http_template["end_point"] = "/channels/" + self.channel_id + "/messages"
        http_template["headers/data"] = message_template

        return await self.user.aiohttp_client_session.http_request(http_template)

    async def get_channel_data(self):
        http_template = await json_and_dictionary_constructor.create_http_request("GET", "/channels/" + self.channel_id, {"Authorization": "Bot " + self.user.bot_data["token"]})

        return await self.user.aiohttp_client_session.http_request(http_template)


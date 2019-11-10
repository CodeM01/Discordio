from json_management import gateway_dictionary_templates

class Channel:

    def __init__(self, user, channel_id):
        self.channel_id = channel_id
        self.user = user

    async def send(self, message):
        http_template = gateway_dictionary_templates.http_load
        message_template = gateway_dictionary_templates.new_message

        message_template["content"] = message
        message_template["tts"] = False

        http_template["request_type"] = "POST"
        http_template["end_point"] = "/channels/" + self.channel_id + "/messages"
        http_template["headers/data"] = message_template

        return await self.user.aiohttp_client_session.http_request(http_template)

    async def get_channel_data(self):
        http_template = gateway_dictionary_templates.http_load

        http_template["request_type"] = "GET"
        http_template["end_point"] = "/channels/" + self.channel_id
        http_template["headers/data"] = {"Authorization": "Bot " + self.user.bot_data["token"]}

        return await self.user.aiohttp_client_session.http_request(http_template)

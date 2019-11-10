from json_management import gateway_dictionary_templates

class Guild:

    def __init__(self, user, guild_id):
        self.guild_id = guild_id
        self.user = user

    async def get_channels(self):
        http_template = gateway_dictionary_templates.http_load

        http_template["request_type"] = "GET"
        http_template["end_point"] = "/guilds/" + self.guild_id + "/channels"
        http_template["headers/data"] = {"Authorization": "Bot " + self.user.bot_data["token"]}

        response = await self.user.aiohttp_client_session.http_request(http_template)
        return response

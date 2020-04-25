import json_and_dictionary_constructor

class Guild:

    def __init__(self, user, guild_id):
        self.guild_id = guild_id
        self.user = user

    async def get_channels(self):
        http_template = await json_and_dictionary_constructor.create_http_request("GET", "/guilds/" + self.guild_id + "/channels", {"Authorization": "Bot " + self.user.bot_data["token"]})

        return await self.user.aiohttp_client_session.http_request(http_template)

class Guild:

    def __init__(self, user, guild_id):
        self.guild_id = guild_id
        self.user = user

    async def get_channels(self):
        load = {"request_type": "GET",
                "end_point": "/guilds/" + self.guild_id + "/channels",
                "headers": {"Authorization": "Bot " + self.user.bot_data["token"]}}

        return await self.user.aiohttp_client_session.http_request(load)

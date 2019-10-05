class Channel:

    def __init__(self, user, guild_id, channel_id):
        self.channel_id = channel_id
        self.guild_id = guild_id

        guild_data = user.guilds[self.guild_id]

        for channel in guild_data["channels"]:
            if channel["id"] == self.channel_id:
                self.data = channel

    @staticmethod
    async def send(content):
        pass

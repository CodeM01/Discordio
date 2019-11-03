class Guild:

    def __init__(self, user, guild_id):
        self.guild_id = guild_id
        self.user = user

    def get_channels(self):
        #request = http_request("guilds/" + self.guild_id + "/channels", "GET",
                               #self.user.bot_data["token"])
        #return request
        pass

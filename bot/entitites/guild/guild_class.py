from RawDiscordBot.api.http_request_class import http_request

class Guild:

    def __init__(self, user, guild_id):
        self.guild_id = guild_id
        self.user = user
        self.response = None

    def get_channels(self):
        request = http_request("https://discordapp.com/api/guilds/" + self.guild_id + "/channels", "GET",
                               self.user.bot_data["token"])
        return request

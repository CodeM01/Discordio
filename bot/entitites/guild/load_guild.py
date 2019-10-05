async def load_guilds(user, input_guilds):
    for guild in input_guilds:
        if not user.guilds.get(guild["id"]):
            # Create Guild
            user.guilds[guild["id"]] = {}

async def load_guild_data(user, guild_data):
    await load_guilds(user, [guild_data])
    user.guilds[guild_data["id"]] = guild_data
    print(user.guilds[guild_data["id"]])

import requests

def http_request(url, type, bot_token=None):
    bot_token = None if bot_token == [] else bot_token

    if type == "GET":
        if bot_token:
            return get_request(url, bot_token)

def get_request(url, bot_token):
    try:
        response = requests.get(url, headers={"Authorization": "Bot " + bot_token}).json()
        return response
    except requests.HTTPError:
        pass
        # I will deal with this later

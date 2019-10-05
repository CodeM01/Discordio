import json
from platform import system

from bot.json import gateway_dictionary_templates as templates


async def create_heartbeat(d):
    template = templates.heart_beat
    template["d"] = d
    return pack(template)

async def create_identify(user):
    template_layout, template_d = templates.basic_layout, templates.identify
    # Putting identify structure into basic structure
    template_layout["d"] = template_d
    # Changing data
    template_layout["d"]["token"] = user.bot_token
    template_layout["d"]["$os"] = system()
    template_layout["op"] = 2
    template_layout["s"] = user.s
    template_layout["t"] = None
    return pack(template_layout)

def pack(dictionary):
    return json.dumps(dictionary)

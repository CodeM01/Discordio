import json
from platform import system

from json_management import gateway_dictionary_templates


async def create_heartbeat(d):
    template = gateway_dictionary_templates.heart_beat
    template["d"] = d
    return pack(template)


async def create_identify(user):
    template_layout = gateway_dictionary_templates.basic_layout
    template_d = gateway_dictionary_templates.identify

    # Putting identify structure into identify load
    template_layout["d"] = template_d

    # Changing data
    template_layout["d"]["token"] = user.bot_data["token"]
    template_layout["d"]["$os"] = system()
    template_layout["op"] = 2
    template_layout["s"] = user.gateway_data["s"]
    template_layout["t"] = None
    return pack(template_layout)


def pack(dictionary):
    return json.dumps(dictionary)

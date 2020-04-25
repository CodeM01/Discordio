import json
from platform import system

import dictionary_templates


async def create_heartbeat(d):
    template = dictionary_templates.heart_beat
    template["d"] = d

    return pack(template)


async def create_identify(user):
    template_layout = dictionary_templates.basic_layout
    template_d = dictionary_templates.identify

    template_layout["d"] = template_d
    template_layout["d"]["token"] = user.bot_data["token"]
    template_layout["d"]["$os"] = system()
    template_layout["op"] = 2
    template_layout["s"] = user.gateway_data["s"]
    template_layout["t"] = None

    return pack(template_layout)

async def create_http_request(request_type, end_point, headers):
    http_template = dictionary_templates.http_load

    http_template["request_type"] = request_type
    http_template["end_point"] = end_point
    http_template["headers/data"] = headers

    """No need to pack as we just need as a dictionary"""
    return http_template

def pack(dictionary):
    return json.dumps(dictionary)

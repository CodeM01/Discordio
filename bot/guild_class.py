#!/usr/bin/python

# Copyright (C) 2010-2013 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from json_management import gateway_dictionary_templates

class Guild:

    def __init__(self, user, guild_id):
        self.guild_id = guild_id
        self.user = user

    async def get_channels(self):
        http_template = gateway_dictionary_templates.http_load

        http_template["request_type"] = "GET"
        http_template["end_point"] = "/guilds/" + self.guild_id + "/channels"
        http_template["headers/data"] = {"Authorization": "Bot " + self.user.bot_data["token"]}

        response = await self.user.aiohttp_client_session.http_request(http_template)
        return response

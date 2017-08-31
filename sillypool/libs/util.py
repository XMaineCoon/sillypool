#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 liangzy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
import json
import requests

from sillypool.libs.useragent import USER_AGENTS
from sillypool.libs.exception import OuterIPError

TEST_IP_URL = 'http://httpbin.org/ip'
TEST_HTTP_URL = 'http://httpbin.org/get?show_env=1'
TEST_HTTPS_URL = 'https://httpbin.org/get?show_env=1'


def make_header():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate'
    }


def get_outer_ip():
    try:
        req = requests.get(url=TEST_IP_URL, headers=make_header(), timeout=5)
        ip = json.loads(req.text)
        return ip['origin']
    except ConnectionError:
        raise OuterIPError


def to_bytes(s):
    if bytes != str:
        if type(s) == str:
            return s.encode('utf-8')
    return s


def to_str(s):
    if bytes != str:
        if type(s) == bytes:
            return s.decode('utf-8')
    return s

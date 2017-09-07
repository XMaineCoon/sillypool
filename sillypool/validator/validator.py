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


from gevent import monkey
monkey.patch_all(thread=False)

import sys
import time
import json
import datetime
import logging
import requests
from gevent.pool import Pool
from sqlalchemy import create_engine

from sillypool.libs.util import make_header, get_outer_ip
from sillypool.libs.util import TEST_HTTP_URL, TEST_HTTPS_URL
from sillypool.libs.exception import InvalidInputTypeError, InvalidResponseError
from sillypool.database.proxydb import ProxyDB


class Validator:
    def __init__(self, config):
        self.config = config
        self.outer_ip = get_outer_ip()
        self.pool = Pool(size=self.config['validator']['size'])

        self.proxydb = ProxyDB('mysql+pymysql://root:mg112233@localhost:3306/proxydb')

    def start(self):
        while True:
            proxys = self.proxydb.

            if proxy_list:
                self.pool.map(self.validate_proxy, proxy_list)
            else:
                time.sleep(60)  # sleep one minute if the db empty

    def stop(self):
        sys.exit()

    def validate_proxy(self, proxy):
        proxies = {"http": "http://%s:%s" % (proxy.ip, proxy.port),
                   "https": "http://%s:%s" % (proxy.ip, proxy.port)}
        protocol = None
        level, desc, speed = self.__check_https_proxy(proxies)
        if level:
            protocol = "https"
        else:
            level, desc, speed = self.__check_http_proxy(proxies)
            if level:
                protocol = "http"

        if protocol:
            proxy.protocol = protocol
            proxy.level = level
            proxy.desc = desc
            proxy.speed = speed
            proxy.valid_times += 1
            proxy.update_time = datetime.datetime.utcnow()
            proxy.save()
        else:
            proxy.delete()

    def __check_http_proxy(self, proxies):
        return self.__check_proxy(proxies, TEST_HTTP_URL)

    def __check_https_proxy(self, proxies):
        return self.__check_proxy(proxies, TEST_HTTPS_URL)

    def __check_proxy(self, proxies, test_url):
        if not isinstance(test_url, str):
            raise InvalidInputTypeError(str)

        try:
            start_time = time.time()
            req = requests.get(url=test_url,
                               headers=make_header(),
                               timeout=self.config['validator']['timeout'],
                               proxies=proxies)
            if req.ok:
                speed = round(time.time() - start_time, 2)
                content = json.loads(req.text)
                origin = content['origin']
                headers = content['headers']

                via = headers.get('Via', None)
                x_forwarded_for = headers.get('X-Forwarded-For', None)
                x_real_ip = headers.get('X-Real-Ip', None)

                if (self.outer_ip in origin) or \
                   (via and self.outer_ip in via) or \
                   (x_forwarded_for and self.outer_ip in x_forwarded_for) or \
                   (x_real_ip and self.outer_ip in x_real_ip):
                    level = 3
                    desc = 'transparent'
                elif via:
                    level = 2
                    desc = 'anonymous'
                else:
                    level = 1
                    desc = 'high anonymous'
                return level, desc, speed

            else:
                raise InvalidResponseError(test_url)
        except (InvalidResponseError, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            return None, None, None
        except Exception as e:
            logging.error(e)
            logging.error("proxy: " + proxies['http'])
            return None, None, None

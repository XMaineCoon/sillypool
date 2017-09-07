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

import logging
import random

import requests

from sillypool.libs.exception import InvalidResponseError
from sillypool.libs.util import make_header
from sillypool.database.base import DBSession
from sillypool.database.models import Proxy


class Downloader:
    def __init__(self, config):
        self.config = config

    def download(self, url):
        try:
            req = requests.get(url=url, headers=make_header(),
                               timeout=self.config['spider']['timeout'])
            if (not req.ok) or len(req.content) < 500:
                raise InvalidResponseError(url)
            else:
                return req.text

        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, InvalidResponseError):
            count = 0
            session = DBSession()
            proxy_list = session.query(Proxy).limit(self.config['spider']['retry']).all()
            session.close()
            while count < self.config['spider']['retry']:
                proxy = random.choice(proxy_list)
                proxies = {"http": "http://%s:%s" % (proxy.ip, proxy.port),
                           "https": "http://%s:%s" % (proxy.ip, proxy.port)}
                try:
                    req = requests.get(url=url, headers=make_header(),
                                       timeout=self.config['spider']['timeout'],
                                       proxies=proxies)
                    if (not req.ok) or len(req.content) < 500:
                        raise InvalidResponseError(url)
                    else:
                        return req.text
                except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, InvalidResponseError):
                    pass
                except Exception as e:
                    logging.error(e)
                    logging.error('url: ' + url)
                finally:
                    count += 1

        return None

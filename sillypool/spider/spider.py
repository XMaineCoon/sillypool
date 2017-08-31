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
import logging
from gevent.pool import Pool
from sqlalchemy import create_engine

from sillypool.common import FREE_PROXY_LIST
from sillypool.database.base import DBSession
from sillypool.database.model import Proxy
from sillypool.spider.parser import Parser
from sillypool.spider.downloader import Downloader


class Spider:
    def __init__(self, config):
        self.config = config
        self.unique = set()
        self.pool = Pool(size=config['spider']['size'])

        # adding addition configuration to DBSession
        engine = create_engine(config['sqlalchemy_uri'], max_overflow=config['spider']['size'])
        DBSession.configure(bind=engine)

    def start(self):
        while True:
            session = DBSession()
            proxy_list = session.query(Proxy).all()
            session.close()
            self.unique.clear()
            for proxy in proxy_list:
                self.unique.add(proxy.ip + ":" + str(proxy.port))

            logging.info('spider unique size: ' + str(len(self.unique)))
            self.pool.map(self.crawl, FREE_PROXY_LIST)

            time.sleep(self.config['spider']['interval'])

    def stop(self):
        sys.exit()

    def crawl(self, url_config):
        try:
            downloader = Downloader(self.config)
            parser = Parser()
            for url in url_config['urls']:
                response = downloader.download(url)
                if response:
                    proxy_list = parser.parse(response, url_config, url)
                    for proxy in proxy_list:
                        tmp = proxy.ip + ":" + str(proxy.port)
                        if tmp not in self.unique:
                            self.unique.add(tmp)
                            proxy.save()
        except Exception as e:
            logging.error(e.args)

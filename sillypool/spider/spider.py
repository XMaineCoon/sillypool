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


import sys
import logging
import grequests
from sillypool.settings import FREE_PROXY_LIST
from sillypool.database.proxydb import ProxyDB
from sillypool.spider.parser import Parser
from sillypool.spider.downloader import Downloader


class Spider:
    def __init__(self, config):
        self.config = config
        self.unique = set()
        self._quit = False

        self.proxydb = ProxyDB('mysql+pymysql://root:mg112233@localhost:3306/proxydb')

    def run(self):
        while not self._quit:
            def exception_handler(request, exception):
                print('Request failed')

            reqs = [
                grequests.get(''),
            ]
            grequests.map(reqs, exception_handler=exception_handler)

    def quit(self):
        self._quit = True

    def start(self):
        while not self._quit:
            self.unique.clear()
            for ip in self.proxydb.load_ip():
                self.unique.add(ip)

            for url_config in FREE_PROXY_LIST:
                self.crawl(url_config)

    def stop(self):
        self._quit = True
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

    @staticmethod
    def _ip2str(ip, port):
        return '{}:{}'.format(ip, port)

    @staticmethod
    def _str2ip(s):
        return s.split(':')

if __name__ == '__main__':
    pass

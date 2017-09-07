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

import datetime
import logging
from lxml.etree import HTML

from sillypool.settings import QQWRY_PATH
from sillypool.database.models import Proxy
from sillypool.libs.exception import ParserTypeNotSupportError
from sillypool.libs.iplocator import IPLocator


class Parser:
    def __init__(self):
        self.ip_locator = IPLocator(QQWRY_PATH)

    def parse(self, response, url_config, url):
        if url_config['type'] == 'xpath':
            return self.parse_xpath(response, url_config, url)
        else:
            raise ParserTypeNotSupportError(url_config['type'])

    def parse_xpath(self, response, url_config, url):
        proxy_list = []
        root = HTML(response)
        proxy_all = root.xpath(url_config['pattern'])
        for proxy in proxy_all:
            try:
                ip = proxy.xpath(url_config['position']['ip'])[0].text
                country, address = self.ip_locator.get_ip_address(self.ip_locator.str2ip(ip))
                proxy = Proxy(
                    ip=proxy.xpath(url_config['position']['ip'])[0].text,
                    port=proxy.xpath(url_config['position']['port'])[0].text,
                    country=self.judge_country(country),
                    area=address,
                    crawl_time=datetime.datetime.utcnow()
                )

                proxy_list.append(proxy)
            except OSError as e:
                logging.error("parser error: " + url)
                break
            except Exception as e:
                logging.error(e)
                logging.error('proxy: ' + proxy)
        return proxy_list

    @staticmethod
    def judge_country(country):
        china_area = ['河北', '山东', '辽宁', '黑龙江', '吉林',
                      '甘肃', '青海', '河南', '江苏', '湖北',
                      '湖南', '江西', '浙江', '广东', '云南',
                      '福建', '台湾', '海南', '山西', '四川',
                      '陕西', '贵州', '安徽', '重庆', '北京',
                      '上海', '天津', '广西', '内蒙', '西藏',
                      '新疆', '宁夏', '香港', '澳门']

        for area in china_area:
            if area in country:
                return "中国"
        return country

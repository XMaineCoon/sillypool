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

import os

# chunzhen ip database's location
QQWRY_PATH = os.path.join(os.path.dirname(__file__), './database/qqwry.dat')


FREE_PROXY_LIST = [
    {
        'urls': ['http://www.66ip.cn/%s.html' % n for n in (['index'] + list(range(2, 12)))],
        'type': 'xpath',
        'pattern': ".//*[@id='main']/div/div[1]/table/tr[position()>1]",
        'position':{'ip': './td[1]', 'port': './td[2]'}
    },
    {
        'urls': ['http://www.66ip.cn/areaindex_%s/%s.html' % (m, n) for m in range(1, 35) for n in range(1, 10)],
        'type': 'xpath',
        'pattern': ".//*[@id='footer']/div/table/tr[position()>1]",
        'position':{'ip': './td[1]', 'port': './td[2]'}
    },
    {
        'urls': ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218'],
        'type': 'xpath',
        'pattern':".//table[@class='sortable']/tbody/tr",
        'position':{'ip': './td[1]', 'port': './td[2]'}
    },
    {
        'urls': ['http://www.mimiip.com/gngao/%s' % n for n in range(1, 10)],
        'type': 'xpath',
        'pattern':".//table[@class='list']/tr",
        'position':{'ip': './td[1]', 'port': './td[2]'}

    },
    {
        'urls': ['http://incloak.com/proxy-list/%s#list' % n for n in (['']+['?start=%s' % (64*m) for m in range(1, 10)])],
        'type': 'xpath',
        'pattern':".//table[@class='proxy__t']/tbody/tr",
        'position':{'ip': './td[1]', 'port': './td[2]', 'type': '', 'protocol': ''}

    },
    {
        'urls': ['http://www.kuaidaili.com/proxylist/%s/' % n for n in range(1, 11)],
        'type': 'xpath',
        'pattern': ".//*[@id='index_free_list']/table/tbody/tr[position()>0]",
        'position':{'ip': './td[1]', 'port': './td[2]', 'type': './td[3]','protocol': './td[4]'}
    },
    {
        'urls': ['http://www.kuaidaili.com/free/%s/%s/' % (m, n) for m in ['inha', 'intr', 'outha', 'outtr'] for n in range(1, 11)],
        'type': 'xpath',
        'pattern': ".//*[@id='list']/table/tbody/tr[position()>0]",
        'position':{'ip': './td[1]', 'port': './td[2]', 'type': './td[3]', 'protocol': './td[4]'}
    },
    {
        'urls': ['http://www.ip181.com/daili/%s.html' % n for n in range(1, 11)],
        'type': 'xpath',
        'pattern': ".//div[@class='row']/div[3]/table/tbody/tr[position()>1]",
        'position':{'ip': './td[1]', 'port': './td[2]', 'type': './td[3]', 'protocol': './td[4]'}

    },
    {
        'urls': ['http://www.xicidaili.com/%s/%s' % (m, n) for m in ['nn', 'nt', 'wn', 'wt'] for n in range(1, 8)],
        'type': 'xpath',
        'pattern': ".//*[@id='ip_list']/tr[position()>1]",
        'position':{'ip': './td[2]', 'port': './td[3]', 'type': './td[5]', 'protocol': './td[6]'}
    },
]


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

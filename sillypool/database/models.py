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
from sqlalchemy import Column, Integer, VARCHAR, DateTime, Numeric
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sillypool.libs.util import ip2str

Base = declarative_base()


class Proxy(Base):
    __tablename__ = 't_proxy'
    __table_args__ = (
        PrimaryKeyConstraint('ip', 'port'),
    )

    ip = Column(VARCHAR(16), nullable=False)                                # IP
    port = Column(Integer, nullable=False)                                  # 端口
    level = Column(Integer, nullable=False, default=0)                      # 匿名等级
    protocol = Column(VARCHAR(100), nullable=False, default='')             # 协议
    crawl_time = Column(DateTime(), default=datetime.datetime.utcnow())     # 爬取时间
    speed = Column(Numeric(5, 2), nullable=False, default=0)                # 速度
    valid_times = Column(Integer, nullable=False, default=0)                # 检验次数
    update_time = Column(DateTime(), default=datetime.datetime.utcnow())    # 更新时间

    def __str__(self):
        return ip2str(self.ip, self.port)


if __name__ == '__main__':
    proxy_d = {
        'ip': '155.155.155.155',
        'port': 1,
        'level': 1
    }
    print(proxy_d)
    print(Proxy(**proxy_d))
    proxy2 = Proxy(**proxy_d)
    print(proxy2)

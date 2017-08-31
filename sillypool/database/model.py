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


from sqlalchemy.ext.declarative import declarative_base

import datetime
from sqlalchemy import Column, Integer, VARCHAR, DateTime, Numeric
from sillypool.database.base import BaseMethod


BaseModel = declarative_base()


class Proxy(BaseModel, BaseMethod):
    __tablename__ = 't_proxy'

    id = Column(Integer, primary_key=True, autoincrement=True)              # ID
    ip = Column(VARCHAR(16), nullable=False)                                # IP
    port = Column(Integer, nullable=False)                                  # 端口
    level = Column(Integer, nullable=False, default=0)                      # 匿名等级
    desc = Column(VARCHAR(100), nullable=False, default='')                 # 描述
    protocol = Column(VARCHAR(100), nullable=False, default='')             # 协议
    country = Column(VARCHAR(100), nullable=False, default='')              # 国家
    area = Column(VARCHAR(100), nullable=False, default='')                 # 地区
    crawl_time = Column(DateTime(), default=datetime.datetime.utcnow())     # 爬取时间
    speed = Column(Numeric(5, 2), nullable=False, default=0)                # 速度
    valid_times = Column(Integer, nullable=False, default=0)                # 检验次数
    update_time = Column(DateTime(), default=datetime.datetime.utcnow())    # 更新时间


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


class Error(Exception):
    # Base class exceptions
    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, self.message)

    def __repr__(self):
        return self.message

    __str__ = __repr__


class InvalidResponseError(Error):
    def __init__(self, url):
        self.message = 'invalid response, url: ' + url
        Error.__init__(self, self.message)


class InvalidInputTypeError(Error):
    def __init__(self, invalid_type):
        self.message = 'invalid input, type: ' + invalid_type
        Error.__init__(self, self.message)


class ParserTypeNotSupportError(Error):
    def __init__(self, not_support_type):
        self.message = 'parse type not support, type: ' + not_support_type
        Error.__init__(self, self.message)


class OuterIPError(Error):
    def __init__(self):
        self.message = 'fail to get out ip'
        Error.__init__(self, self.message)

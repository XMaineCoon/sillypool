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
import sys
import json
import getopt
import logging
import traceback

from functools import wraps

from sillypool import __version__

VERBOSE_LEVEL = 5

verbose = 0
logger_level = 0


def check_python():
    info = sys.version_info
    if info[0] == 3 and not info[1] >= 4:
        print('Python 3.4+ required')
        sys.exit(1)
    elif info[0] not in [3]:
        print('Python version not supported')
        sys.exit(1)


def print_exception(e):
    global verbose
    logging.error(e)
    if verbose > 0:
        import traceback
        traceback.print_exc()


def exception_handle(self_, err_msg=None, exit_code=None,
                     destroy=False, conn_err=False):
    # self_: if function passes self as first arg

    def process_exception(e, self=None):
        print_exception(e)
        if err_msg:
            logging.error(err_msg)
        if exit_code:
            sys.exit(1)

        if not self_:
            return

        if conn_err:
            addr, port = self._client_address[0], self._client_address[1]
            logging.error('%s when handling connection from %s:%d' %
                          (e, addr, port))
        if self._config['verbose']:
            traceback.print_exc()
        if destroy:
            self.destroy()

    def decorator(func):
        if self_:
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                try:
                    func(self, *args, **kwargs)
                except Exception as e:
                    process_exception(e, self)
        else:
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    process_exception(e)

        return wrapper
    return decorator


def find_config_path():
    # config_dev.json is used in the development environment
    config_path = os.path.join(os.path.dirname(__file__), 'config_dev.json')
    if os.path.exists(config_path):
        return config_path

    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_path):
        return config_path
    return None


def set_logger_config():
    global logger_level
    logging.basicConfig(level=logger_level,
                        format='%(asctime)s %(levelname)s: %(filename)s[line:%(lineno)d] - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')


def check_config(config):
    if config.get('daemon', None) == 'stop':
        # no need to specify configuration for daemon stop
        return

    if config['spider']['size'] > 30:
        logging.warning('warning: spider pool size %d too large' % config['spider']['size'])

    if config['validator']['size'] > 30:
        logging.warning('warning: validator pool size %d too large' % config['validator']['size'])


def get_config():
    global verbose
    global logger_level

    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-s: %(message)s')

    shortopts = 'hvc:d:'
    longopts = ['help', 'version']

    try:
        config_path = find_config_path()
        optlist, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
        for key, value in optlist:
            if key == '-c':
                config_path = value

        if config_path:
            logging.info('loading config from %s' % config_path)

            with open(config_path, 'r') as f:
                config = json.load(f)

        v_count = 0
        for key, value in optlist:
            if key in ('-h', '--help'):
                print_help()
                sys.exit(0)
            elif key == '--version':
                print_version()
                sys.exit(0)
            elif key == '-v':
                v_count += 1
                # '-vv' turns on more verbose mode
                config['verbose'] = v_count
            elif key == '-d':
                config['daemon'] = value
    except getopt.GetoptError as e:
        print(e, file=sys.stderr)
        print_help()
        sys.exit(2)

    if not config:
        logging.error('config not specified')
        print_help()
        sys.exit(2)

    # make the default config
    config['spider']['interval'] = int(config['spider'].get('interval', 1))
    config['spider']['size'] = int(config['spider'].get('size', 1))
    config['spider']['timeout'] = int(config['spider'].get('timeout', 1))
    config['spider']['retry'] = int(config['spider'].get('retry', 1))

    config['validator']['size'] = int(config['validator'].get('size', 1))
    config['validator']['timeout'] = int(config['validator'].get('timeout', 1))

    config['pid_file'] = config.get('pid_file', '/var/run/sillypool.pid')
    config['log_file'] = config.get('log_file', '/var/log/sillypool.log')
    config['verbose'] = config.get('verbose', False)

    config['mysql']['user'] = config['mysql'].get('user', 'root')
    config['mysql']['password'] = config['mysql'].get('password', '')
    config['mysql']['host'] = config['mysql'].get('host', 'localhost')
    config['mysql']['port'] = int(config['mysql'].get('port', 3306))
    config['mysql']['dbname'] = config['mysql'].get('dbname', 'sillypool')
    # make the sqlalchemy_uri
    config['sqlalchemy_uri'] = 'mysql+pymysql://%s:%s@%s:%d/%s?charset=utf8' % (
        config['mysql']['user'], config['mysql']['password'],
        config['mysql']['host'], config['mysql']['port'],
        config['mysql']['dbname'])
    config['sqlalchemy_uri'] = 'sqlite:////E:/sillypool/sillypool/test.db'
    logging.info(config['sqlalchemy_uri'])

    # logger setting
    logging.getLogger('').handlers = []
    logging.addLevelName(VERBOSE_LEVEL, 'VERBOSE')
    if config['verbose'] >= 2:
        logger_level = VERBOSE_LEVEL
    elif config['verbose'] == 1:
        logger_level = logging.DEBUG
    elif config['verbose'] == -1:
        logger_level = logging.WARN
    elif config['verbose'] <= -2:
        logger_level = logging.ERROR
    else:
        logger_level = logging.INFO
    verbose = config['verbose']
    set_logger_config()

    check_config(config)

    return config


def print_help():
    print('''usage: server [OPTION]...
a simple http/https proxy pool.

You can supply configurations via either config file or command line arguments.

Proxy Pool option:
  -c CONFIG                 path to config file

General options:
  -h, --help                show this help message and exit
  -d start/stop/restart     daemon mode
  -v, -vv                   verbose mode
  --version                 show version information

Online help: <https://github.com/liangzy-gh/sillypool>
''')


def print_version():
    print(__version__)

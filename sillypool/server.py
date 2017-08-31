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
import os
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.path.pardir))

from sillypool import shell
from sillypool import daemon


def run_spider(config):
    from sillypool.spider import Spider

    try:
        spider = Spider(config)
        spider.start()
    except KeyboardInterrupt:
        sys.exit(1)

    import signal

    def handler(signum, _):
        logging.info('spider doing shutting down..')
        spider.stop()
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)


def run_validator(config):
    from sillypool.validator import Validator

    try:
        validator = Validator(config)
        validator.start()
    except KeyboardInterrupt:
        sys.exit(1)

    import signal

    def handler(signum, _):
        logging.info('validator doing shutting down..')
        validator.stop()
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)


def run_webui():
    from sillypool.webui.app import app

    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        sys.exit(1)

    import signal

    def handler(signum, _):
        logging.info('webui doing shutting down..')
        app.quit()
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)


def main():
    shell.check_python()

    config = shell.get_config()

    daemon.daemon_exec(config)

    if os.name == 'posix':
        children = []
        is_child = False

        r = os.fork()
        if r == 0:
            logging.info('spider started')
            is_child = True
            run_spider(config)
        else:
            children.append(r)

            r = os.fork()
            if r == 0:
                logging.info('validator started')
                is_child = True
                run_validator(config)
            else:
                children.append(r)

                r = os.fork()
                if r == 0:
                    logging.info('webui started')
                    is_child = True
                    run_webui()
                else:
                    children.append(r)

        if not is_child:
            import signal

            def handler(signum, _):
                for pid in children:
                    try:
                        os.kill(pid, signum)
                        os.waitpid(pid, 0)
                    except OSError:  # child may already exited
                        pass
                sys.exit()
            signal.signal(signal.SIGTERM, handler)
            signal.signal(signal.SIGINT, handler)

            for child in children:
                os.waitpid(child, 0)

    else:
        # There is no platform independent way to implement os.fork().
        # So use multiprocess instead
        try:
            from multiprocessing import Process

            processes = list()

            processes.append(Process(target=run_spider, args=(config, ), name="spider"))
            processes.append(Process(target=run_validator, args=(config, ), name="validator"))
            processes.append(Process(target=run_webui, args=(), name='webui'))

            for process in processes:
                process.daemon = True
                process.start()

            for process in processes:
                process.join()
        except KeyboardInterrupt:
            sys.exit(1)


if __name__ == '__main__':
    main()

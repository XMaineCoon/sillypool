# -*- coding: utf-8 -*-

import time
from gevent import monkey
monkey.patch_all(time=True)


def echo(i):
    time.sleep(1-i*0.1)
    print(i)
    return i


from gevent.pool import Pool

p = Pool(5)
run1 = [a for a in p.imap_unordered(echo, range(10))]
run2 = [a for a in p.imap_unordered(echo, range(10))]
run3 = [a for a in p.imap_unordered(echo, range(10))]
run4 = [a for a in p.imap_unordered(echo, range(10))]

print(run1 == run2 == run3 == run4)

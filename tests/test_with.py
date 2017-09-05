# -*- coding: utf-8 -*-


from contextlib import contextmanager


@contextmanager
def make_context():
    print('enter')
    try:
        print('1')
        yield {}
        print('2')
    except RuntimeError as err:
        print(err)
    finally:
        print('exit')

with make_context() as value:
    print(type(value))

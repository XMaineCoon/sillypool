# -*- coding: utf-8 -*-

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from sillypool.database.models import Base, Proxy
from sillypool.libs.util import ip2str


class ProxyDB:
    def __init__(self, url):
        self.url = make_url(url)
        self.engine = create_engine(self.url, echo=False)
        self.Session = sessionmaker(bind=self.engine)

        self.create_db()
        self.init_db()

    def create_db(self):
        """
        create database base on url if not exist
        :return:
        """
        if not self.url.database:
            return
        database = self.url.database
        self.url.database = None
        engine = create_engine(self.url, poolclass=NullPool)
        conn = engine.connect()
        try:
            conn.execute('CREATE DATABASE %s' % database)
        except SQLAlchemyError:
            pass
        finally:
            conn.close()
            self.url.database = database

    def init_db(self):
        """
        initialization all tables
        :return:
        """
        Base.metadata.create_all(self.engine)

    def drop_db(self):
        """
        drop all tables
        :return:
        """
        Base.metadata.drop_all(self.engine)

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def add(self, obj):
        with self.session_scope() as session:
            proxy = Proxy(**obj)
            session.add(proxy)

    def add_all(self, obj_all):
        with self.session_scope() as session:
            proxy_all = [Proxy(**obj) for obj in obj_all]
            session.add_all(proxy_all)

    def merge(self, obj):
        with self.session_scope() as session:
            proxy = Proxy(**obj)
            session.merge(proxy)

    def merge_all(self, obj_all):
        with self.session_scope() as session:
            proxy_all = [Proxy(**obj) for obj in obj_all]
            for proxy in proxy_all:
                session.merge(proxy)

    def delete(self, ip, port):
        with self.session_scope() as session:
            proxy = Proxy(ip=ip, port=port)
            session.delete(proxy)

    def delete_all(self, obj_all):
        with self.session_scope() as session:
            proxy_all = [Proxy(**obj) for obj in obj_all]
            for proxy in proxy_all:
                session.delete(proxy)

    def load_ip(self):
        """
        load all ip from proxy db
        :return: ['ip:port', 'ip2:port2']
        """
        with self.session_scope() as session:
            for ip, port in session.query(Proxy.ip, Proxy.port):
                yield ip2str(ip, port)

    def _select2dict(self):
        pass


if __name__ == '__main__':
    proxydb = ProxyDB('mysql+pymysql://root:mg112233@localhost:3306/proxydb')

    import time
    ps1 = [{'ip': '127.0.0.1', 'port': port} for port in range(10000)]
    start = time.time()
    proxydb.merge_all(ps1)
    print(time.time() - start)
    # for a in proxydb.load_ip():
    #     print(a)
    #
    # print(Proxy.__table__.insert())
    # print(Proxy.__table__.update())
    # print(Proxy.__table__.delete())
    # print(Proxy.__table__.select())

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import struct

# this module is form
# http://qicheng0211.blog.51cto.com/3958621/1589442


class IPLocator:
    def __init__(self, ip_db_file):
        self.cur_start_ip = None
        self.cur_end_ip = None
        self.cur_end_ip_offset = None

        self.ip_db = open(ip_db_file, "rb")
        s = self.ip_db.read(8)
        (self.first_index, self.last_index) = struct.unpack('II', s)
        self.index_count = int((self.last_index - self.first_index) / 7 + 1)

    def get_version(self):
        s = self.get_ip_address(0xffffff00)
        return s

    def get_area_address(self, offset=0):
        if offset:
            self.ip_db.seek(offset)
        s = self.ip_db.read(1)
        (byte,) = struct.unpack('B', s)
        if byte == 0x01 or byte == 0x02:
            p = self.get_long3()
            if p:
                return self.get_string(p)
            else:
                return ""
        else:
            self.ip_db.seek(-1, 1)
            return self.get_string(offset)

    def get_address(self, offset, ip=0):
        self.ip_db.seek(offset + 4)
        s = self.ip_db.read(1)
        (byte,) = struct.unpack('B', s)
        if byte == 0x01:
            country_offset = self.get_long3()
            self.ip_db.seek(country_offset)
            s = self.ip_db.read(1)
            (b,) = struct.unpack('B', s)
            if b == 0x02:
                country_address = self.get_string(self.get_long3())
                self.ip_db.seek(country_offset + 4)
            else:
                country_address = self.get_string(country_offset)
            area_address = self.get_area_address()
        elif byte == 0x02:
            country_address = self.get_string(self.get_long3())
            area_address = self.get_area_address(offset + 8)
        else:
            country_address = self.get_string(offset + 4)
            area_address = self.get_area_address()
        return country_address, country_address + area_address

    def dump(self, first, last):
        if last > self.index_count:
            last = self.index_count
        for index in range(first, last):
            offset = self.first_index + index * 7
            self.ip_db.seek(offset)
            buf = self.ip_db.read(7)
            (ip, of1, of2) = struct.unpack("IHB", buf)
            country, address = self.get_address(of1 + (of2 << 16))

    def set_ip_range(self, index):
        offset = self.first_index + index * 7
        self.ip_db.seek(offset)
        buf = self.ip_db.read(7)
        (self.cur_start_ip, of1, of2) = struct.unpack("IHB", buf)
        self.cur_end_ip_offset = of1 + (of2 << 16)
        self.ip_db.seek(self.cur_end_ip_offset)
        buf = self.ip_db.read(4)
        (self.cur_end_ip,) = struct.unpack("I", buf)

    def get_ip_address(self, ip):
        l = 0
        r = self.index_count - 1
        while l < r - 1:
            m = int((l + r) / 2)
            self.set_ip_range(m)
            if ip == self.cur_start_ip:
                l = m
                break
            if ip > self.cur_start_ip:
                l = m
            else:
                r = m
        self.set_ip_range(l)
        # version information, 255.255.255.X, urgy but useful
        if ip & 0xffffff00 == 0xffffff00:
            self.set_ip_range(r)
        if self.cur_start_ip <= ip <= self.cur_end_ip:
            address = self.get_address(self.cur_end_ip_offset)
        else:
            address = "IP address not found"
        return address

    def get_ip_range(self, ip):
        self.get_ip_address(ip)
        r = self.ip2str(self.cur_start_ip) + ' - ' \
            + self.ip2str(self.cur_end_ip)
        return r

    def get_string(self, offset=0):
        if offset:
            self.ip_db.seek(offset)
        s = b''
        ch = self.ip_db.read(1)
        (byte,) = struct.unpack('B', ch)
        while byte != 0:
            s += ch
            ch = self.ip_db.read(1)
            (byte,) = struct.unpack('B', ch)
        return s.decode('gbk')

    @staticmethod
    def ip2str(ip):
        return str(ip >> 24) + '.' + str((ip >> 16) & 0xff) + '.' + str((ip >> 8) & 0xff) + '.' + str(ip & 0xff)

    @staticmethod
    def str2ip(s):
        (ip,) = struct.unpack('I', socket.inet_aton(s))
        return ((ip >> 24) & 0xff) | ((ip & 0xff) << 24) | ((ip >> 8) & 0xff00) | ((ip & 0xff00) << 8)

    def get_long3(self, offset=0):
        if offset:
            self.ip_db.seek(offset)
        s = self.ip_db.read(3)
        (a, b) = struct.unpack('HB', s)
        return (b << 16) + a


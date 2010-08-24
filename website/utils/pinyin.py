#!/usr/bin/python
# -*- coding: cp936 -*-
# $Id$
# Copyright yefe<yefe@ichuzhou.cn>
import os


def stoi(s):
    h = '0x'
    for i in s: h += hex(ord(i))[-2:]
    return int(h, 16)

class Hanzi2Pinyin:
    def __init__(self):
        "Load data table"
        try:
            fp = open(os.path.normpath(os.path.join(os.path.dirname(__file__), 'pinyin.txt')))
        except IOError:
            raise Exception("Can't load data from pinyin.txt\nPlease make sure this file exists.")
        else:
            self.data = fp.read()
            self.table = {}
            for l in self.data.split('\n'):
                self.table[l[0:2]] = l[2:]
            fp.close()

    def convert(self, value):
        "Convert GB2312 to PinYin"
        pinyin = []
        tASCII = ''
        # 字符检查
        for c in value:
            if c == ' ':
                if len(tASCII):
                    pinyin.append(tASCII)
                tASCII = ''
            try:
                i = stoi(c.encode('gb2312'))
            except UnicodeEncodeError:
                continue
            # 48-57 (0-9)    65-90(A-Z)    97-122(a-z)    gb2312汉字部分
            if (i>=48 and i<=57) or (i>=65 and i<=90) or (i>=97 and i<=122):
                tASCII += c
            elif i>=0xb0a1 and i<=0xfffe and i not in (0xbfff,0xcfff,0xdfff,0xefff):
                try:
                    p = self.table[c.encode('gb2312')]
                    pinyin.append(p)
                except IndexError:
                    pass
        if tASCII != '':
            pinyin.append(tASCII)
        return pinyin


if __name__ == '__main__':
    print Hanzi2Pinyin().convert(u'你                   。，%……#￥#@@#￥Y^#@$#@%^%*&^&*               好12 345 Big Pig   ')



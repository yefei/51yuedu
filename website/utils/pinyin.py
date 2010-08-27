# -*- coding: utf-8 -*-
# $Id$
# Copyright 2010 Yefe<yefe@ichuzhou.cn>
from os import path
import codecs


class Hanzi2Pinyin(object):
    def __init__(self):
        self.table = {}
        try:
            fp = codecs.open(path.join(path.dirname(__file__), 'pinyin.txt'), 'r', 'utf-8')
        except IOError:
            raise Exception("Can't load data from pinyin.txt")
        except UnicodeDecodeError:
            raise Exception("Can't decode data from pinyin.txt")
        else:
            for l in fp.readlines():
                self.table[l[0]] = l[1:-1]
            fp.close()

    def convert(self, value):
        pinyin = []
        tASCII = ''
        # 字符检查
        for c in value.lower() + ' ': # 加个空格多一次循环 修正尾部字符丢失问题
            i = ord(c)
            if (i >= 48 and i <= 57) or (i >= 97 and i <= 122): # 48-57[0-9]   97-122[a-z]
                tASCII += c
                continue

            tASCII and pinyin.append(tASCII)
            tASCII = ''

            if self.table.has_key(c):
                pinyin.append(self.table[c])

        return pinyin


if __name__ == '__main__':
    import time
    t = u'Prep 你好    中 国！I Love China! 2010年8月 !@    #   $%^   &* ()_+   Append'
    s = time.time()
    p = Hanzi2Pinyin() # you class
    print 'init:', time.time() - s
    print '-'.join(p.convert(t)) # you convert
    s = time.time()
    for i in xrange(0,10000):
        p.convert(t) # you convert
    print 'convert:', time.time() - s



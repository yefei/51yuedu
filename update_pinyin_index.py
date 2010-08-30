# -*- coding: utf-8 -*-
# Created on 2010-8-27
# @author: Yefe
# $Id$
import MySQLdb
from MySQLdb.cursors import DictCursor
from website.utils.pinyin import Hanzi2Pinyin


db = MySQLdb.connect(user='root', db='51yuedu')
db.set_character_set('utf8')


def get_all_author():
    global db
    cursor = db.cursor(DictCursor)
    cursor.execute("SELECT id,name FROM book_author WHERE pyindex = 0")
    data = cursor.fetchall()
    cursor.close()
    return data


if __name__ == '__main__':
    p = Hanzi2Pinyin()
    i = list('-ABCDEFGHIJKLMNOPQRSTUVWXYZ*')
    for a in get_all_author():
        c = db.cursor()
        pyindex = p.convert(a['name'].decode('utf-8'))[0][0].upper()
        pyindex = i.index(pyindex)
        c.execute('UPDATE book_author SET pyindex = %s WHERE id = %s', (pyindex, a['id']))
        c.close()

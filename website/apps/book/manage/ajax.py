# -*- coding: utf-8 -*-
# Created on 2010-6-15
# @author: Yefe
# $Id$
from django.contrib.ajax import ajax
from django.contrib.ajax.utils import param
from website.apps.book.models import Book, Chapter
from website.apps.account.auth import api_admin_required


@ajax
def search_book(request, response):
    title = param(request, 'title', unicode)
    if title:
        s = Book.search_title.query(title).set_options(passages=True, mode='SPH_MATCH_ALL').all()[0:10]
        if s:
            return [{'id':v.id, 'title':v.sphinx['passages']['title'], 'author':v.author} for v in s]


@ajax
@api_admin_required
def delete_chapter(request, response):
    id = param(request, 'id', int)
    Chapter.objects.filter(id=id).delete()


# -*- coding: utf-8 -*-
# Created on 2010-6-8
# @author: Yefe
# $Id$
from django.db import models
from django.contrib.ajax import ajax, AjaxError
from django.contrib.ajax.utils import param
from website.apps.account.auth import api_login_required
from website.apps.book.models import Book, Chapter, ReadPoint


BOOK_RATE_MAX = 5
BOOK_RATE_MIN = -5


def _get_book(id):
    try:
        return Book.objects.get(pk=id)
    except:
        raise AjaxError(u'小说不存在')

@ajax
@api_login_required
def set_rate(request, response):
    id = param(request, 'id', int)
    rate = param(request, 'rate', int)
    if rate == 0 or rate > BOOK_RATE_MAX or rate < BOOK_RATE_MIN:
        raise AjaxError(u'评分不正确')
    book = _get_book(id)
    if book.check_rated(request.user):
        raise AjaxError(u'你已经给此小说评过分了')
    
    book.book_rate_set.create(user=request.user, rate=rate) # 记录已评分
    
    # 计算帖子平均分值
    #sum = book.book_rate_set.aggregate(models.Sum('rate'))[ 'rate__sum' ] or 0
    #count = book.rate_count + 1
    Book.objects.filter(pk=book.pk).update(rate_score=models.F('rate_score')+rate,
                                           rate_count=models.F('rate_count')+1)


@ajax
def stat(request, response):
    id = param(request, 'id', int)
    Book.objects.filter(pk=id).update(views=models.F('views')+1)

@ajax
@api_login_required
def save_point(request, response):
    chapter_id = param(request, 'chapter_id', int)
    try:
        chapter = Chapter.objects.select_related('book').get(pk=chapter_id)
    except:
        raise AjaxError(u'Chapter 不存在')
    point, is_create = ReadPoint.objects.get_or_create(user=request.user, book=chapter.book)
    point.chapter = chapter
    point.save()

@ajax
@api_login_required
def delete_point(request, response):
    id = param(request, 'id', int)
    request.user.book_readpoint_set.filter(id=id).delete()


@ajax
@api_login_required
def favorite(request, response):
    id = param(request, 'id', int)
    book = _get_book(id)
    try:
        request.user.book_favorite_set.create(book=book)
    except:
        raise AjaxError('你已经收藏过了。')


@ajax
@api_login_required
def delete_favorite(request, response):
    id = param(request, 'id', int)
    request.user.book_favorite_set.filter(id=id).delete()



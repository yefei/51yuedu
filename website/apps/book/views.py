# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.utils.hashcompat import sha_constructor
from django.conf import settings
from datetime import datetime
from website.apps.book.models import Subarea, Category, Book, Chapter
from website.utils.pagination import TemplateRESTPaginator, TemplatePaginator
from website.apps.account.auth import login_required
from website.apps.book.forms import ReviewForm
from website.utils.captcha import CaptchaForm


@render
def index(request, page=1):
    books = Book.objects.select_related('subarea','category')
    books = TemplateRESTPaginator(books, 'book:index_page', [], page=page, per_page=100)
    return 'book/index.html', locals()

@render
def books(request, subarea_id=None, category_id=None, page=1):
    if subarea_id:
        subarea = get_object_or_404(Subarea, id=subarea_id)
        category = None
        books = subarea.book_set.all()
        r = 'book:books_subarea_page'
        r_args = (subarea.id,)
    elif category_id:
        category = get_object_or_404(Category.objects.select_related('subarea'), id=category_id)
        subarea = category.subarea
        books = category.book_set.all()
        r = 'book:books_category_page'
        r_args = (category.id,)
    else:
        return redirect('book:index')
    categories = {}
    for c in subarea.book_category_set.values():
        categories[c['id']] = c
    books = TemplateRESTPaginator(books, r, r_args, page=page, per_page=100)
    return 'book/books.html', locals()

"""
def number2chinese(number):
    units = u'  十百千万十百千亿十百千万兆十百千万亿' # 单位数组 
    numeric = u'零一二三四五六七八九' # 中文数字数组
    s = u''
    number = str(number)
    for i in range(0, len(number)):
        s += numeric[int(number[i])]
        if units[len(number)-i] != u' ':
            s += units[len(number)-i]
    s = s.rstrip(u'零')
    if s[0:2] == u'一十':
        s = s[1:]
    return s
"""

@render
def show(request, id, slug=None):
    book = get_object_or_404(Book.objects.select_related('subarea','category'), id=id)
    subarea = book.subarea
    category = book.category
    vol = []
    chapter = {}
    for c in book.book_chapter_set.all():
        if c.vol_number not in vol:
            vol.append(c.vol_number)
            chapter[c.vol_number] = []
        chapter[c.vol_number].append(c)
    
    # 评分
    if request.user.is_authenticated():
        try:
            user_rate = book.book_rate_set.get(user=request.user)
        except:pass
    # 显示前几个评分
    #rate_list = book.book_rate_set.select_related('user')[:10]
    book_review = book.book_review_set.select_related('user')
    return 'book/show.html', locals()

@render
def chapter(request, id):
    chapter = get_object_or_404(Chapter.objects.select_related('book'), id=id)
    book = chapter.book
    try:
        prev_chapter = Chapter.objects.filter(book=book, id__lt=chapter.id).order_by('-id')[0]
    except:
        prev_chapter = None
    try:
        next_chapter = Chapter.objects.filter(book=book, id__gt=chapter.id).order_by('id')[0]
    except:
        next_chapter = None
    return 'book/chapter.html', locals()


@render
def review(request, id):
    book = get_object_or_404(Book.objects.select_related('subarea','category'), id=id)
    subarea = book.subarea
    category = book.category
    review = book.book_review_set.select_related('user')
    review = TemplatePaginator(review, request)
    return 'book/review.html', locals()


@login_required
@render
def review_new(request, id):
    book = get_object_or_404(Book.objects.select_related('subarea','category'), id=id)
    subarea = book.subarea
    category = book.category
    if request.is_post():
        form = ReviewForm(book=book, user=request.user, data=request.POST)
        if form.is_valid():
            review = form.save()
            return HttpResponseRedirect('%s?page=last#post%s' % (reverse('book:review', args=(book.id,)), review.id))
    else:
        form = ReviewForm(book=book, user=request.user)
    return 'book/review_new.html', locals()


@login_required
@render
def read_point(request):
    books = request.user.book_readpoint_set.select_related('book','chapter','book__subarea','book__category')
    books = TemplatePaginator(books, request)
    return 'book/read_point.html', locals()

@login_required
@render
def favorite(request):
    books = request.user.book_favorite_set.select_related('book','book__subarea','book__category')
    books = TemplatePaginator(books, request)
    return 'book/favorite.html', locals()


def make_download_key(book_id, session_key):
    return sha_constructor(settings.SECRET_KEY + str(book_id) + session_key).hexdigest()

@render
def download(request, id):
    book = get_object_or_404(Book.objects.select_related('subarea','category'), id=id)
    subarea = book.subarea
    category = book.category
    key = None
    if request.is_post():
        form = CaptchaForm(request.session, data=request.POST)
        if form.is_valid():
            key = make_download_key(book.id, request.session.session_key)
    else:
        form = CaptchaForm(request.session)
    return 'book/download.html', locals()


@render
def download_start(request, id, encode, format):
    if request.GET.has_key('key') and \
        request.GET['key'] == make_download_key(id, request.session.session_key):
        pass
    else:
        return HttpResponseForbidden()
    
    book = get_object_or_404(Book.objects.select_related('subarea','category'), id=id)
    content = [
        u'小说：《%s》' % book.title,
        u'作者：%s' % book.author_name,
        u'分类：%s/%s' % (book.subarea.label, book.category.label),
        u'更新：%s' % book.updated_at,
        u'下载：%s' % datetime.now(),
        u'编码：%s' % encode,
        u'网址：http://www.51yuedu.com/book/%s/' % book.id,
    ]
    for c in book.book_chapter_set.all():
        content += [
            '','',
            c.title,
            '-------------------------------------',
            c.content.replace('\n', '\r\n'),
        ]
    resp = HttpResponse('\r\n'.join(content).encode(encode), mimetype='text/plain')
    resp['Content-Disposition'] = 'attachment; filename="%s.txt"' % book.title.encode('gbk')
    return resp



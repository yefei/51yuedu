# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import permalink, signals
from django.contrib.sphinxsearch.models import SphinxSearch
from website.apps.book import chapter_db
from website.apps.account.models import User
from website.utils.pinyin import Hanzi2Pinyin


pinyin = Hanzi2Pinyin()


class Subarea(models.Model):
    label       = models.CharField(u'标签', max_length=32)
    order_index = models.SmallIntegerField(u'排序', default=0)

    class Meta:
        ordering = ('order_index',)
        verbose_name = verbose_name_plural = u'小说分区'

    def __unicode__(self):
        return self.label

    @permalink
    def get_absolute_url(self):
        return ('book:books_subarea', (self.id,))


class Category(models.Model):
    subarea     = models.ForeignKey(Subarea, related_name='book_category_set')
    label       = models.CharField(u'标签', max_length=32)
    order_index = models.SmallIntegerField(u'排序', default=0)

    class Meta:
        ordering = ('order_index',)
        verbose_name = verbose_name_plural = u'小说分类'

    def __unicode__(self):
        return u'%s > %s' % (self.subarea.label, self.label)

    @permalink
    def get_absolute_url(self):
        return ('book:books_category', (self.id,))

class Author(models.Model):
    category    = models.ForeignKey(Category, related_name='author_set')
    name        = models.CharField(u'姓名', max_length=32)
    pyindex     = models.SmallIntegerField(u'读音索引', choices=zip(range(0,28),tuple('-ABCDEFGHIJKLMNOPQRSTUVWXYZ*')), default=0)
    is_hot      = models.BooleanField(u'热门', default=False, db_index=True)


class Book(models.Model):
    subarea     = models.ForeignKey(Subarea, related_name='book_set', editable=False)
    category    = models.ForeignKey(Category, related_name='book_set')
    author      = models.ForeignKey(Author, related_name='author_set')
    author_name = models.CharField(u'作者', max_length=32)
    title       = models.CharField(u'标题', max_length=255)
    series      = models.CharField(u'系列', max_length=255, blank=True)
    part        = models.CharField(u'主角', max_length=255, blank=True)
    length      = models.PositiveIntegerField(u'字数', default=0, editable=False)
    views       = models.PositiveIntegerField(u'查看数', default=0, db_index=True)
    rate_score  = models.IntegerField(u'总分', default=0, db_index=True, editable=False)
    rate_count  = models.PositiveIntegerField(u'评分次数', default=0, db_index=True, editable=False)
    updated_at  = models.DateTimeField(u'更新时间', null=True, blank=True,
                                       db_index=True, editable=False)
    is_complete = models.BooleanField(u'已完本', default=False, db_index=True)

    search_title    = SphinxSearch(index='title')
    search_author   = SphinxSearch(index='author')

    class Meta:
        #ordering = ('-id',)
        verbose_name = verbose_name_plural = u'小说'
    
    @permalink
    def get_absolute_url(self):
        return ('book:slug_show', (self.id, '-'.join(pinyin.convert(self.title))))
    
    def check_rated(self, user):
        return self.book_rate_set.filter(user=user).exists()

    @property
    def rate_average(self):
        if self.rate_score == 0 or self.rate_count == 0:
            return 0
        return self.rate_score / self.rate_count

class BookDescription(models.Model):
    book        = models.ForeignKey(Book, related_name='book_description_set')
    content     = models.TextField(u'描述内容')


class Rate(models.Model):
    book        = models.ForeignKey(Book, related_name='book_rate_set')
    user        = models.ForeignKey(User, related_name='book_rate_set')
    rate        = models.SmallIntegerField(u'分值')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = verbose_name_plural = u'小说评分'


class Chapter(models.Model):
    book        = models.ForeignKey(Book, related_name='book_chapter_set', editable=False)
    vol_number  = models.PositiveSmallIntegerField(u'卷号', default=1)
    vol_name    = models.CharField(u'卷名', max_length=255, null=True, blank=True)
    title       = models.CharField(u'标题', max_length=255)
    length      = models.PositiveSmallIntegerField(u'字数', default=0, editable=False)
    size        = models.PositiveSmallIntegerField(u'大小', default=0, editable=False)
    created_at  = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ('id',)
        verbose_name = verbose_name_plural = u'小说章节'

    @property
    def content(self):
        c = chapter_db.client.get(str(self.id))
        return c and c.decode('utf-8') or u''

    def set_content(self, content):
        ascii_content = content.encode('utf-8')
        self.length = len(content)
        self.size = len(ascii_content)
        return chapter_db.client.set(str(self.id), ascii_content, min_compress_len=1024)

def chapter_post_delete_signal(instance, *args, **kw):
    # 更新对应小说的字数
    Book.objects.filter(pk=instance.book.pk).update(length=models.F('length')-len(instance.content))
    chapter_db.client.delete(str(instance.pk))
signals.post_delete.connect(chapter_post_delete_signal, Chapter)



class Review(models.Model):
    book        = models.ForeignKey(Book, related_name='book_review_set')
    user        = models.ForeignKey(User, related_name='book_review_set')
    content     = models.TextField(u'内容')
    created_at  = models.DateTimeField(u'发布时间', auto_now_add=True)

    class Meta:
        ordering = ('id',)
        verbose_name = verbose_name_plural = u'小说评论'


class ReadPoint(models.Model):
    user            = models.ForeignKey(User, related_name='book_readpoint_set')
    book            = models.ForeignKey(Book, related_name='book_readpoint_set')
    chapter         = models.ForeignKey(Chapter, related_name='book_readpoint_set', null=True, blank=True)
    started_at      = models.DateTimeField(u'开始于', auto_now_add=True)
    last_read_at    = models.DateTimeField(u'最后阅读于', auto_now=True, db_index=True)

    class Meta:
        ordering = ('-last_read_at',)
        verbose_name = verbose_name_plural = u'阅读进度'


class Favorite(models.Model):
    user        = models.ForeignKey(User, related_name='book_favorite_set')
    book        = models.ForeignKey(Book, related_name='book_favorite_set')
    created_at  = models.DateTimeField(u'收藏于', auto_now_add=True)

    class Meta:
        unique_together = ('user','book')
        ordering = ('id',)
        verbose_name = verbose_name_plural = u'我的收藏'













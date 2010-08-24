# -*- coding: utf-8 -*-
# Created on 2010-4-12
# @author: Yefe
# $Id$
from datetime import datetime, timedelta
from django.db import models
from django.db.models import signals
from django.db.models.query import QuerySet
from django.utils.hashcompat import sha_constructor


ONLINE_TIMEOUT = 60 * 15


class UserQuerySet(QuerySet):
    def filter_online(self, is_online=True):
        t = datetime.now() - timedelta(seconds=ONLINE_TIMEOUT)
        if not is_online:
            return self.filter(last_request_at__lt=t)
        return self.filter(is_login=True, last_request_at__gt=t)
    
    def filter_age(self, age=None, *args, **kwargs):
        if age is None and len(kwargs) == 0:
            assert self.query.can_filter(), "Cannot filter a query once a slice has been taken."
        t = datetime.today().date()
        q = {}
        if age:
            q['birthday'] = t - timedelta(365*age)
        else:
            for k,v in kwargs.items():
                q['birthday__%s' % k] = t - timedelta(365*v)
        return self.filter(**q)

class UserManager(models.Manager):
    def get_query_set(self):
        return UserQuerySet(self.model)
    
    def filter_online(self, *args, **kwargs):
        return self.get_query_set().filter_online(*args, **kwargs)
    
    def filter_age(self, *args, **kwargs):
        return self.get_query_set().filter_age(*args, **kwargs)
    
    def create_user(self, username, email, password=None):
        "Creates and saves a User with the given username, e-mail and password."
        user = self.model(None, username, '', '', email.strip().lower())
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def get_by_expr(self, expr):
        if ':' in expr:
            type, value = expr.split(':')
            if type == 'id':
                return self.get(pk=value)
            if type == 'username':
                expr = value
        return self.get(username=expr)

class User(models.Model):
    GENDER_CHOICES = (
        ('M', u'男'),
        ('F', u'女'),
    )
    
    username            = models.CharField(u'用户名', max_length=24, unique=True)
    crypted_password    = models.CharField(max_length=45)
    email               = models.EmailField(u'电子邮件')
    
    gender              = models.CharField(u'性别', max_length=1, choices=GENDER_CHOICES, blank=True)
    birthday            = models.DateField(u'生日', null=True, blank=True)
    
    is_login            = models.BooleanField(u'已登录?', default=False, db_index=True)
    is_admin            = models.BooleanField(u'管理员?', default=False, db_index=True)
    
    online_seconds      = models.PositiveIntegerField(u'在线秒数', default=0)
    
    last_request_at     = models.DateTimeField(u'最后请求时间', auto_now_add=True, db_index=True)
    registered_at       = models.DateTimeField(u'注册日期', auto_now_add=True)
    login_ip            = models.IPAddressField(u'登录IP', null=True, blank=True)
    login_at            = models.DateTimeField(u'登录日期', null=True, blank=True)
    
    ######################
    book_auto_save_point = models.BooleanField(u'自动保存小说阅读记录', default=True)
    ######################
    
    objects             = UserManager()
    
    class Meta:
        verbose_name = verbose_name_plural = u'用户'
    
    def __unicode__(self):
        return u'%d: %s' % (self.id, self.username)
    
    def is_authenticated(self):
        return True
    
    def set_password(self, password):
        from random import choice
        salt = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(5)])
        self.crypted_password = salt + sha_constructor(salt + password).hexdigest()
    
    def check_password(self, password):
        return len(self.crypted_password) == 45 and \
            sha_constructor(self.crypted_password[:5] + password).hexdigest() == self.crypted_password[5:]
    
    @property
    def age(self):
        if self.birthday:
            return datetime.today().year - self.birthday.year
        return None
    
    @property
    def is_online(self):
        return self.is_login and not self.is_invisible \
            and (self.last_request_at + timedelta(seconds=ONLINE_TIMEOUT)) > datetime.now()
    
    def login(self, request):
        self.login_ip = request.META['REMOTE_ADDR']
        self.login_at = datetime.now()
        self.is_login = True
        User.objects.filter(pk=self.pk).update(
            login_ip = self.login_ip,
            login_at = self.login_at,
            is_login = self.is_login
        )
    
    def logout(self):
        self.is_login = False
        User.objects.filter(pk=self.pk).update(
            is_login = self.is_login
        )

# 未登陆则返回此类
class AnonymousUser(object):
    def is_authenticated(self):
        return False

class UserField(models.OneToOneField):
    "User OneToOneField auto create and delete"
    
    def __init__(self, **kwargs):
        super(UserField, self).__init__(to=User, **kwargs)
    
    def contribute_to_class(self, cls, name):
        self.model = cls
        super(UserField, self).contribute_to_class(cls, name)
        signals.post_save.connect(self.instance_post_save, sender=User)
        signals.post_delete.connect(self.instance_post_delete, sender=User)
    
    def instance_post_save(self, instance, created, *args, **kwargs):
        if created:
            self.model._base_manager.create(**{self.get_attname():instance.pk})
    
    def instance_post_delete(self, instance, *args, **kwargs):
        self.model._base_manager.filter(**{self.get_attname():instance.pk}).delete()




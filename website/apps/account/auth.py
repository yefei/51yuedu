# -*- coding: utf-8 -*-
# Created on 2010-4-9
# @author: Yefe
# $Id$
import time
from functools import wraps
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.utils.hashcompat import sha_constructor
from django.utils.http import urlquote, cookie_date
from django.core.urlresolvers import reverse
from django.contrib.ajax.exceptions import AjaxError
from website.apps.account.models import User, AnonymousUser


AUTHENTICATE_SESSION_KEY = 'account_user_id'
AUTHENTICATE_COOKIE_KEY = 'account_auth_token'
AUTHENTICATE_TOKEN_MAX_AGE = 60 * 60 * 24 * 30 # 默认验证有效期


# 根据用户名和密码验证用户
def authenticate(username, password):
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        pass
    return None

# 生成一个 authenticate_token 密匙
def authenticate_token_key(user_id, crypted_password, expires_at):
    return sha_constructor('%d%s%d' % (user_id, crypted_password, expires_at)).hexdigest()

# 返回一个 authenticate_token 字符串
# expires_at 是一个 unix秒数
def authenticate_token(user, expires_at):
    key = authenticate_token_key(user.id, user.crypted_password, expires_at)
    return '%d$%s$%d' % (user.id, key, expires_at)

# 验证一个 authenticate_token 并返回一个用户对象
def get_user_from_authenticate_token(value):
    try:
        id, key, expires_at = value.split('$')
        if int(expires_at) > time.time():
            user = User.objects.get(pk=int(id))
            if key == authenticate_token_key(user.id, user.crypted_password, int(expires_at)):
                return user
    except:
        pass
    return None

def login(request, user):
    user.login(request)
    request.user = user
    request.session[AUTHENTICATE_SESSION_KEY] = user.id

def logout(request):
    request.user.is_authenticated() and request.user.logout()
    request.user = AnonymousUser()
    del request.session[AUTHENTICATE_SESSION_KEY]

def login_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        else:
            path = urlquote(request.get_full_path())
            tup = reverse('account:login'), path
            return HttpResponseRedirect('%s?next=%s' % tup)
    return wraps(view_func)(_wrapped_view_func)

def admin_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return wraps(view_func)(_wrapped_view_func)

def api_login_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise AjaxError('login_required')
        return view_func(request, *args, **kwargs)
    return wraps(view_func)(_wrapped_view_func)

def api_admin_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_admin:
            return view_func(request, *args, **kwargs)
        raise AjaxError('admin_required')
    return wraps(view_func)(_wrapped_view_func)

def store_login_cookie(response, user, max_age=AUTHENTICATE_TOKEN_MAX_AGE):
    expires_at = int(time.time() + max_age)
    token = authenticate_token(user, expires_at)
    response.set_cookie(AUTHENTICATE_COOKIE_KEY, token, expires=cookie_date(expires_at))

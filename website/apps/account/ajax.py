# -*- coding: utf-8 -*-
'''
Created on 2009-10-17
$Id$
@author: Yefe
'''
from django.contrib.ajax import ajax, AjaxError
from django.contrib.ajax.utils import param
from website.apps.account.validators import \
    validate_username as _validate_username, \
    validate_username_uniqueness as _validate_username_uniqueness, \
    ValidationError
from website.apps.account.forms import AuthenticationForm
from website.apps.account.auth import login as _login, logout as _logout, store_login_cookie


@ajax
def validate_username_uniqueness(request, response):
    username = param(request, 'username', unicode)
    try:
        _validate_username(username)
        _validate_username_uniqueness(username)
        return {'message':u'用户名可以使用', 'valid':True}
    except ValidationError, e:
        return {'message':u','.join(e.messages), 'valid':False}


@ajax
def login(request, response):
    form = AuthenticationForm(request.REQUEST)
    if form.is_valid():
        user = form.get_user()
        _login(request, user)
        if form.cleaned_data['remberme']:
            store_login_cookie(response, user)
    else:
        assert AjaxError(form.errors)

@ajax
def logout(request, response):
    _logout(request)



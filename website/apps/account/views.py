# -*- coding: utf-8 -*-
# $Id$
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from website.apps.account.auth import login_required, \
    login as _login, logout as _logout, store_login_cookie
from website.apps.account.forms import AuthenticationForm, RegisterForm
from website.utils.captcha import CaptchaForm

@login_required
@render
def index(request):
    read_books = request.user.book_readpoint_set.count()
    return 'account/index.html', locals()

@render
def login(request):
    if request.is_post():
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            next = request.REQUEST.get('next', reverse('account:index'))
            _login(request, user)
            resp = HttpResponseRedirect(next)
            if form.cleaned_data['remberme']:
                store_login_cookie(resp, user)
            return resp
    else:
        form = AuthenticationForm()
    return 'account/login.html', locals()

@render
def logout(request):
    _logout(request)
    next = request.REQUEST.get('next', reverse('account:index'))
    return HttpResponseRedirect(next)

@render
def register(request):
    if request.user.is_authenticated():
        return 'account/registered.html', locals()
    
    if request.is_post():
        captcha = CaptchaForm(request.session, data=request.POST)
        form = RegisterForm(request.POST)
        if captcha.is_valid() and form.is_valid():
            user = form.save()
            _login(request, user)
            return 'account/register_done.html', locals()
    else:
        captcha = CaptchaForm(request.session)
        form = RegisterForm()
    return 'account/register.html', locals()


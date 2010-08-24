# -*- coding: utf-8 -*-
# Create by: Yefe @ 2009-8-17
# $Id$
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from website.apps.account.auth import login_required
from website.apps.account.setting.forms import ProfileForm, \
    AvatarForm, PasswordForm, EmailForm, FunctionForm

@login_required
@render
def index(request):
    return HttpResponseRedirect(reverse('account:setting:function'))

@login_required
@render
def function(request):
    if request.is_post():
        form = FunctionForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = FunctionForm(instance=request.user)
    return 'account/setting/function.html', locals()

@login_required
@render
def profile(request):
    if request.is_post():
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=request.user)
    return 'account/setting/profile.html', locals()

@login_required
@render
def avatar(request):
    if request.is_post():
        form = AvatarForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = AvatarForm(request.user)
    return 'account/setting/avatar.html', locals()

@login_required
@render
def password(request):
    if request.is_post():
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
    else:
        form = PasswordForm(request.user)
    return 'account/setting/password.html', locals()

@login_required
@render
def email(request):
    if request.is_post():
        form = EmailForm(request.user, request.POST)
        if form.is_valid():
            form.save()
    else:
        form = EmailForm(request.user)
    return 'account/setting/email.html', locals()



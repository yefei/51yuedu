# -*- coding: utf-8 -*-
# Create by: Yefe @ 2009-8-19
# $Id$
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from website.apps.account.models import User
from website.utils.captcha import CaptchaForm
from website.apps.account.setting.forms import SetPasswordForm
from website.apps.account.tokens import base36_to_int, PasswordResetTokenGenerator
from website.apps.account.forgot.forms import PasswordResetForm

@render
def index(request):
    form = PasswordResetForm(request)
    if request.is_post():
        captcha = CaptchaForm(request.session, data=request.POST)
        if captcha.is_valid():
            form = PasswordResetForm(request, data=request.POST)
            if form.is_valid():
                form.save()
    else:
        captcha = CaptchaForm(request.session)
    return 'account/forgot/index.html', locals()


@render
def confirm(request, uidb36=None, token=None):
    assert uidb36 is not None and token is not None
    try:
        uid_int = base36_to_int(uidb36)
    except ValueError:
        raise Http404
    
    user = get_object_or_404(User, id=uid_int)
    token_generator = PasswordResetTokenGenerator()
    form = SetPasswordForm(None)
    
    if token_generator.check_token(user, token):
        validlink = True
        if request.is_post():
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
    else:
        validlink = False
    
    return 'account/forgot/confirm.html', locals()


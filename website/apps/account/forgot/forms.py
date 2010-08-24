# -*- coding: utf-8 -*-
# Create by: Yefe @ 2009-8-19
# $Id$
from django import forms
from django.core.mail import send_mail
from django.template.loader import get_template
from website.apps.account.models import User
from website.apps.account.validators import validate_username
from website.apps.account.tokens import PasswordResetTokenGenerator, int_to_base36


class PasswordResetForm(forms.Form):
    username    = forms.CharField(label=u'用户名', validators=[validate_username])
    email       = forms.EmailField(label=u"E-mail", help_text=u"填入你的账号所绑定的电子邮件地址")
    
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            self.user_cache = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(u"该用户名不存在。你确定已经注册过了？")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if not email == self.user_cache.email:
            raise forms.ValidationError(u"您输入的电子邮件和当前账号所绑定的不一致。")
        return email
    
    def save(self):
        token_generator = PasswordResetTokenGenerator()
        t = get_template('account/forgot/password_reset_email.html')
        c = {
            'request': self.request,
            'uid': int_to_base36(self.user_cache.id),
            'user': self.user_cache,
            'token': token_generator.make_token(self.user_cache),
        }
        send_mail(u"密码重设", t.render(c), None, [self.user_cache.email])

PasswordResetForm.base_fields.keyOrder = ['username','email']



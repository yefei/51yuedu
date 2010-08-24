# -*- coding: utf-8 -*-
# Create by: Yefe @ 2009-8-17
# $Id$
from django import forms
from website.apps.account.models import User
from website.apps.account.validators import validate_username, validate_username_uniqueness


class RegisterForm(forms.ModelForm):
    username                 = forms.CharField(label=u"用户名", validators=[validate_username, validate_username_uniqueness])
    password                 = forms.CharField(label=u"密码", min_length=6, max_length=20, widget=forms.PasswordInput, help_text=u'请输入6至20位字符')
    password_confirmation    = forms.CharField(label=u"密码确认", widget=forms.PasswordInput, help_text=u'重复上面输入的密码')
    email                    = forms.EmailField(label=u"电子邮件", max_length=75, help_text=u"输入一个你常用的电子邮件用于找回密码")

    class Meta:
        model = User
        fields = ("username", "email")
    
    def clean_email(self):
        return self.cleaned_data["email"].lower()

    def clean_password_confirmation(self):
        password = self.cleaned_data.get("password", "")
        password_confirmation = self.cleaned_data["password_confirmation"]
        if password != password_confirmation:
            raise forms.ValidationError(u"和上面输入的密码不一致")
        return password_confirmation

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit: user.save()
        return user

RegisterForm.base_fields.keyOrder = ['username','password','password_confirmation','email']


class AuthenticationForm(forms.Form):
    username        = forms.CharField(label=u'用户名', validators=[validate_username])
    password        = forms.CharField(label=u'密码', widget=forms.PasswordInput)
    remberme        = forms.BooleanField(label=u'记住我', required=False)
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) == 0:
            raise forms.ValidationError(u'请输入用户名')
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) == 0:
            raise forms.ValidationError(u'请输入密码')
        return password

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            try:
                self.user_cache = User.objects.get(username=username)
            except User.DoesNotExist:
                self.user_cache = None
            if self.user_cache is None:
                raise forms.ValidationError(u'用户名不存在，确定注册过了吗？')
            elif not self.user_cache.check_password(password):
                raise forms.ValidationError(u'密码错误')
        return self.cleaned_data
    
    def get_user(self):
        return self.user_cache


class UsernameConfirmationForm(forms.Form):
    username                = forms.CharField(label=u'用户名', validators=[validate_username])
    username_confirmation   = forms.CharField(label=u'用户名确认')

    def clean_username_confirmation(self):
        username = self.cleaned_data.get("username", "")
        username_confirmation = self.cleaned_data["username_confirmation"]
        if username != username_confirmation:
            raise forms.ValidationError(u"和上面输入的用户名不一致")
        return username_confirmation


class UsernameForm(forms.Form):
    username = forms.CharField(label=u'用户名', validators=[validate_username])



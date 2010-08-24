# -*- coding: utf-8 -*-
# Create by: Yefe @ 2009-8-19
# $Id$
from django import forms
from website.apps.account.models import User
from PIL import Image; Image.preinit()

IMAGE_SUPPORT_FORMAT = ', '.join(Image.OPEN.keys())


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('gender','birthday')

class FunctionForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('book_auto_save_point',)


class AvatarForm(forms.Form):
    avatar = forms.ImageField(label=u"上传头像图片", help_text=u"支持的图像文件格式: %s" % (IMAGE_SUPPORT_FORMAT))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AvatarForm, self).__init__(*args, **kwargs)

    def save(self):
        f = self.cleaned_data["avatar"]
        if f is not None:
            import os
            from website.settings import PUBLIC_ROOT

            avatar_path = os.path.join(PUBLIC_ROOT, 'avatar')

            def resize(im, size, format="PNG", **params):
                # preserve aspect ratio
                re_w, re_h = size
                im_w, im_h = im.size
                if im_w < im_h:
                    if im_w > re_w: im_h = max(im_h * re_w / im_w, 1); im_w = re_w
                    #crop = 0, (im_h - re_h) / 2, re_w, (im_h - re_h) / 2 + re_h # 取中间部分
                    crop = 0, 0, re_w, re_h # 从顶部取
                else:
                    if im_h > re_h: im_w = max(im_w * re_h / im_h, 1); im_h = re_h
                    crop = (im_w - re_w) / 2, 0, (im_w - re_w) / 2 + re_w, re_h

                im = im.resize((im_w, im_h), Image.ANTIALIAS)
                im = im.crop(crop)

                path = os.path.join(avatar_path, str(size[0]))
                if not os.path.exists(path):
                    os.makedirs(path)

                filename = os.path.join(path, '%d.png' % self.user.pk)
                im.save(filename, format, **params)

            im = Image.open(f).convert(mode='RGB')
            resize(im, (160,200))
            resize(im, (120,120))
            resize(im, (100,100))
            resize(im, (80,80))
            resize(im, (60,60))
            resize(im, (50,50))
            resize(im, (40,40))
            resize(im, (30,30))
            resize(im, (20,20))


class SetPasswordForm(forms.Form):
    new_password                = forms.CharField(label=u'新密码', min_length=6, max_length=20, widget=forms.PasswordInput)
    new_password_confirmation   = forms.CharField(label=u'确认密码', min_length=6, max_length=20, widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password_confirmation(self):
        password1 = self.cleaned_data.get('new_password')
        password2 = self.cleaned_data.get('new_password_confirmation')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(u'两次输入的密码不一致')
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password'])
        if commit:
            self.user.save()
        return self.user

SetPasswordForm.base_fields.keyOrder = ['new_password','new_password_confirmation']


class PasswordForm(SetPasswordForm):
    old_password = forms.CharField(label=u'原始密码', widget=forms.PasswordInput)

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(u'原始密码不正确')
        return old_password

PasswordForm.base_fields.keyOrder = ['new_password','new_password_confirmation','old_password']


class EmailForm(forms.Form):
    password = forms.CharField(label=u"密码", widget=forms.PasswordInput)
    old_email = forms.EmailField(label=u"原始邮件地址", max_length=75)
    new_email = forms.EmailField(label=u"新邮件地址", max_length=75)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EmailForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not self.user.check_password(password):
            raise forms.ValidationError(u"密码不正确。请重新输入")
        return password

    def clean_old_email(self):
        old_email = self.cleaned_data["old_email"]
        if not self.user.email == old_email.lower():
            raise forms.ValidationError(u"原始邮件地址不正确。请重新输入")
        return old_email

    def save(self, commit=True):
        self.user.email = self.cleaned_data['new_email'].lower()
        if commit:
            self.user.save()
        return self.user

EmailForm.base_fields.keyOrder = ['password','old_email','new_email']











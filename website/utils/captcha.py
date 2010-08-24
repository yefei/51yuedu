# -*- coding: utf-8 -*-
# Create by: Yefe @ 2009-8-19
# $Id$
import os, random
from glob import glob
from random import choice
from cStringIO import StringIO
from PIL import Image, ImageColor, ImageDraw, ImageFont
from django.http import HttpResponse
from django import forms


WIDTH = 80
HEIGHT = 26
CODES = 4

FONT = ImageFont.truetype(os.path.normpath(os.path.join(os.path.dirname(__file__), 'captcha_font.ttf')), 18)
CHARS = 'ABCDEFGHJKLMNPRSTWXZV234568'
BGCOLOR = ImageColor.getrgb('#E0E8F3')
COLOR = ImageColor.getrgb('#333')
IM = Image.new('RGB', (WIDTH, HEIGHT), BGCOLOR)


def make(request):
    im = IM.copy()
    draw = ImageDraw.Draw(im)
    code = ''.join([choice(CHARS) for i in range(CODES)])
    draw.text((10, 0), code, fill=COLOR, font=FONT)
    request.session['captcha'] = code.lower()
    buf = StringIO()  
    im.save(buf, 'png')
    buf.closed
    return HttpResponse(buf.getvalue(), 'image/png')


class CaptchaForm(forms.Form):
    captcha = forms.CharField(label=u'验证码', min_length=4, max_length=4)
    
    def __init__(self, session, *args, **kwargs):
        self.session = session
        super(CaptchaForm, self).__init__(*args, **kwargs)

    def clean_captcha(self):
        captcha = self.cleaned_data['captcha'].lower()
        if not self.session.has_key('captcha') or not captcha == self.session['captcha']:
            raise forms.ValidationError(u"验证码不正确")
        if self.session.has_key('captcha'):
            del self.session['captcha']
        return captcha

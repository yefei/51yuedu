# -*- coding: utf-8 -*-
# Created on 2010-4-9
# @author: Yefe
# $Id$
from django.core.exceptions import ValidationError

from website.utils import stoi
from website.apps.account.models import User

# 用户名长度限制
# 长度计算规则: 英文算一个字符中文算两个字符
USERNAME_MIN_LENGTH = 4   # 最短
USERNAME_MAX_LENGTH = 16  # 最长


class UsernameValidator(object):
    message = u'用户名不正确'
    code = 'invalid'
    
    def __call__(self, value):
        # 长度检查
        try:
            l = len(value.encode('gb2312'))
        except UnicodeEncodeError:
            raise ValidationError(self.message, code=self.code)
        if l < USERNAME_MIN_LENGTH:
            raise ValidationError(u'用户名太短', code=self.code)
        if l > USERNAME_MAX_LENGTH:
            raise ValidationError(u'用户名过长', code=self.code)
        
        # 字符检查
        for c in value:
            try:
                i = stoi(c.encode('gb2312'))
            except UnicodeEncodeError:
                raise ValidationError(self.message, code=self.code)
            # 48-57 (0-9)    65-90(A-Z)    97-122(a-z)    gb2312汉字部分
            if ((i>=48 and i<=57) or (i>=65 and i<=90) or (i>=97 and i<=122)) or \
               (i>=0xb0a1 and i<=0xfffe and i not in (0xbfff,0xcfff,0xdfff,0xefff)):
                pass
            else:
                raise ValidationError(self.message, code=self.code)


validate_username = UsernameValidator()

def validate_username_uniqueness(value):
    if User.objects.filter(username=value).exists():
        raise ValidationError(u"用户名 %s 已经被占用" % value)

def validate_username_exists(value):
    if not User.objects.filter(username=value).exists():
        raise ValidationError(u"用户名 %s 不存在" % value)



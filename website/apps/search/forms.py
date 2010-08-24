# -*- coding: utf-8 -*-
# Created on 2010-3-17
# @author: Yefe
# $Id$
from django import forms
from django.contrib.sphinxsearch.models import SphinxQuerySet

from website.apps.account.models import User
from website.apps.book.models import Book


class SearchForm(forms.Form):
    MODE_CHOICES = (
        (0, u'任意匹配'),
        (1, u'全部匹配'),
        (2, u'高级搜索'),
    )
    
    word        = forms.CharField(label=u'关键词', required=False, initial='')
    mode        = forms.ChoiceField(label=u'模式', required=False, choices=MODE_CHOICES, initial=0)
    
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.search = SphinxQuerySet(index='*')
    
    def clean_word(self):
        word = self.cleaned_data['word'].strip()
        if len(word) > 0:
            return word
        return None
    
    def clean_mode(self):
        mode = int(self.cleaned_data['mode'] or 0)
        return {0:'SPH_MATCH_ANY', 1:'SPH_MATCH_ALL', 2:'SPH_MATCH_EXTENDED2'}[mode]
    
    def is_valid(self):
        return super(SearchForm, self).is_valid() and self.cleaned_data['word']
    
    def query(self):
        return self.search.query(self.cleaned_data['word']).set_options(passages=True, mode=self.cleaned_data['mode'])

class UserFilterForm(SearchForm):
    user = forms.CharField(required=False, label=u'用户过滤', help_text=u'输入用户名或用户编号')
    
    def clean_user(self):
        user = self.cleaned_data['user']
        if user:
            if user.isdigit():
                user_id = int(user)
            else:
                try:
                    user_id = User.objects.get(username=user).pk
                except User.DoesNotExist:
                    raise forms.ValidationError(u'用户不存在')
            self.search = self.search.filter(user_id=user_id)
        return user


class BookSearchForm(SearchForm):
    def __init__(self, *args, **kwargs):
        super(BookSearchForm, self).__init__(*args, **kwargs)
        self.search = Book.search
    
    def query(self):
        return super(BookSearchForm, self).query().select_related('subarea','category')







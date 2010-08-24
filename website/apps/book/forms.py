# -*- coding: utf-8 -*-
# Created on 2010-6-8
# @author: Yefe
# $Id$
from django import forms
from website.apps.book.models import Review



class ReviewForm(forms.ModelForm):
    content = forms.CharField(label=u'评论内容', max_length=3000, min_length=2, widget=forms.Textarea)
    
    class Meta:
        model = Review
        fields = ("content", )
    
    def __init__(self, book, user, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.instance.book = book
        self.instance.user = user

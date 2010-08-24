# -*- coding: utf-8 -*-
# Created on 2010-6-8
# @author: Yefe
# $Id$
from datetime import datetime
from django import forms
from django.db.models import F
from website.apps.book.models import Book, Category, Chapter



class BookForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.select_related('subarea').order_by('subarea'),
                                      cache_choices=True, label=u'分类')

    class Meta:
        model = Book
        fields = ("category", 'title', 'author_name', 'series', 'part', 'is_complete')

    def save(self):
        self.instance.subarea = self.instance.category.subarea
        return super(BookForm, self).save()


class ChpaterForm(forms.ModelForm):
    content = forms.CharField(label=u'内容', max_length=1024*512, widget=forms.Textarea)

    class Meta:
        model = Chapter
        fields = ("vol_number", 'vol_name', 'title')

    def __init__(self, *args, **kwargs):
        if kwargs.has_key('instance'):
            self.base_fields['content'].initial = kwargs['instance'].content
        else:
            self.base_fields['content'].initial = ''
        super(ChpaterForm, self).__init__(*args, **kwargs)

    def save(self):
        o = super(ChpaterForm, self).save()
        org_len = len(o.content)
        o.set_content(self.cleaned_data['content'])
        o.created_at = datetime.now()
        diff_length = o.length - org_len
        Book.objects.filter(pk=o.book.pk).update(length=F('length')+diff_length, updated_at=o.created_at)
        return o.save()


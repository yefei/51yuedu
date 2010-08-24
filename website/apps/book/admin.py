# -*- coding: utf-8 -*-
# Created on 2010-5-29
# @author: Yefe
# $Id$
from datetime import datetime
from django import forms
from django.db.models import F
from django.contrib import admin
from django.core.urlresolvers import reverse
from website.apps.book.models import Category, Subarea, Book, Chapter


class CategoryInline(admin.TabularInline):
    model = Category
    fk_name = 'subarea'

class SubareaAdmin(admin.ModelAdmin):
    list_display = ('label', 'order_index')
    list_editable = ('order_index',)
    inlines = (CategoryInline,)


def chapter_link(obj):
    return u'<a href="%s?book__id__exact=%s" target="admin_chapter%s">查看</a>' % (
                reverse('django_admin:model_book_chapter:changelist'), obj.pk, obj.pk)
chapter_link.short_description = u'章节'
chapter_link.allow_tags = True

class ChapterInline(admin.TabularInline):
    model = Chapter
    fk_name = 'book'

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author_name', 'length', 'views', 'rate_score', 'rate_count', 'updated_at', chapter_link)
    list_filter = ('subarea', 'category')
    search_fields = ('=title',)
    inlines = (ChapterInline,)
    
    def save_model(self, request, obj, form, change):
        obj.subarea = obj.category.subarea
        obj.save()


class ChapterAdminForm(forms.ModelForm):
    content = forms.CharField(label=u'内容', max_length=1024*512, widget=forms.Textarea)
    class Meta:
        model = Chapter
    
    def __init__(self, *args, **kwargs):
        if kwargs.has_key('instance'):
            self.base_fields['content'].initial = kwargs['instance'].content
        else:
            self.base_fields['content'].initial = ''
        super(ChapterAdminForm, self).__init__(*args, **kwargs)

def chapter_title_link(obj):
    return u'<a href="%s" target="admin_chapter_edit%s">%s</a>' % (
                reverse('django_admin:model_book_chapter:change', args=(obj.pk,)), obj.pk, obj.title)
chapter_title_link.short_description = u'标题'
chapter_title_link.allow_tags = True

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('id', chapter_title_link, 'vol_number', 'vol_name', 'length', 'size', 'created_at')
    form = ChapterAdminForm
    
    def save_model(self, request, obj, form, change):
        org_len = len(obj.content)
        obj.set_content(form.cleaned_data['content'])
        diff_length = obj.length - org_len
        Book.objects.filter(pk=obj.book.pk).update(length=F('length')+diff_length, updated_at=datetime.now())
        obj.save()


admin.site.register(Subarea, SubareaAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)

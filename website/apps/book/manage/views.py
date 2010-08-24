# -*- coding: utf-8 -*-
# Created on 2010-6-15
# @author: Yefe
# $Id$
from django.shortcuts import render, redirect, get_object_or_404
from website.apps.account.auth import admin_required
from website.apps.book.manage.forms import BookForm, ChpaterForm
from website.apps.book.models import Book, Chapter


@admin_required
@render
def index(request):
    return 'book/manage/index.html', locals()


@admin_required
@render
def add(request):
    if request.is_post():
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return redirect('book:manage:book', book.id)
    else:
        form = BookForm()
    return 'book/manage/add.html', locals()


@admin_required
@render
def book(request, id):
    book = get_object_or_404(Book.objects.select_related('subarea','category'), id=id)
    return 'book/manage/book.html', locals()


@admin_required
@render
def delete(request, id):
    book = get_object_or_404(Book.objects.select_related('subarea','category'), id=id)
    if request.is_post():
        book.delete()
        return redirect('book:manage:index')
    return 'book/manage/delete.html', locals()


@admin_required
@render
def chapter(request, id):
    chapter = get_object_or_404(Chapter.objects.select_related('book'), id=id)
    if request.is_post():
        form = ChpaterForm(instance=chapter, data=request.POST)
        if form.is_valid():
            form.save()
            save_success = True
    else:
        form = ChpaterForm(instance=chapter)
    return 'book/manage/chapter.html', locals()


@admin_required
@render
def chapter_add(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.is_post():
        form = ChpaterForm(data=request.POST)
        form.instance.book = book
        if form.is_valid():
            form.save()
            return redirect('book:manage:book', book.id)
    else:
        form = ChpaterForm()
        try:
            c = book.book_chapter_set.latest('vol_number')
            form.base_fields['vol_number'].initial = c.vol_number
        except:
            pass
    return 'book/manage/chapter_add.html', locals()


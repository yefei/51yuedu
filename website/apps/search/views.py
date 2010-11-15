# -*- coding: utf-8 -*-
# Created on 2010-3-17
# @author: Yefe
# $Id$
from django.shortcuts import render
from django.http import Http404
from django.contrib.sphinxsearch.models import SearchError
from website.apps.search.forms import SearchForm, BookSearchForm, AuthorSearchForm
from website.utils.pagination import TemplatePaginator


APP_FORMS = {
    'book': BookSearchForm,
    'author': AuthorSearchForm,
}

APP_NAMES = {
    'book': u'书名',
    'author': u'作者',
}

@render
def index(request):
    form = SearchForm(request.REQUEST)
    if form.is_valid():
        try:
            results = form.query()
            if results: pass
            results_list = TemplatePaginator(results, request)
        except SearchError, e:
            results = None
            results_error = e
    return 'search/index.html', locals()

@render
def app(request, applabel, word=None):
    if not APP_FORMS.has_key(applabel):
        raise Http404()
        #return redirect('search:index')
    data = request.REQUEST.copy()
    results = None
    if word is not None and len(word):
        #word = unquote_plus(str(word)).decode('utf-8')
        data.dicts = list(data.dicts)
        data.dicts.append({'word':word})
    form = APP_FORMS[applabel](data)
    if form.is_valid():
        try:
            results = form.query()
            if results: pass
            results_list = TemplatePaginator(results, request)
        except SearchError, e:
            results = None
            results_error = e
    return ('%s/search.html' % applabel, 'search/app_%s.html' % applabel, 'search/index.html'), locals()



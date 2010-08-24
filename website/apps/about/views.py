# -*- coding: utf-8 -*-
from django.shortcuts import render
from website.apps.about.forms import FeedbackForm

# Create your views here.

@render
def feedback(request):
    success = False
    if request.is_post():
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.instance.ip = request.META.get('REMOTE_ADDR','--')
            form.save()
            success = True
    else:
        form = FeedbackForm()
    return 'about/feedback.html', locals()


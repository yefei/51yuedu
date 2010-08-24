# -*- coding: utf-8 -*-
# Created on 2010-6-13
# @author: Yefe
# $Id$
from django import forms
from website.apps.about.models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("name", "contact", 'content')
    
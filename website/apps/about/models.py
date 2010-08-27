# -*- coding: utf-8 -*-
from django.db import models



class Feedback(models.Model):
    name        = models.CharField(u'姓名', max_length=24, blank=True, help_text=u'可不填')
    contact     = models.CharField(u'联系方式', max_length=120, blank=True, help_text=u'可不填')
    content     = models.TextField(u'留言内容')
    created_at  = models.DateTimeField(u'发布时间', auto_now_add=True)
    ip          = models.IPAddressField(u'IP')

    class Meta:
        ordering = ('-id',)
        verbose_name = verbose_name_plural = u'留言/反馈'



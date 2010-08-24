# -*- coding: utf-8 -*-
# Created on 2010-6-6
# @author: Yefe
# $Id$
from website.utils.memcachedb import Client
from django.conf import settings

client = Client(settings.MEMCACHEDB, debug=0)



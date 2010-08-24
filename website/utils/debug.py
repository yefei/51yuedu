# -*- coding: utf-8 -*-
# Create by: Yefe @ 2009-8-20
# $Id$
from pprint import pformat
import re
import sys
from datetime import datetime
from django.db import connection

PUBLIC_RULE = re.compile(r'^/public/', re.IGNORECASE)


class DebugMiddleware(object):
    def process_response(self, request, response):
        if PUBLIC_RULE.findall(request.path): return response

        print >> sys.stderr, "[%s] %s: %s" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), request.method, request.get_full_path())

        if len(request.GET) > 0:
            print "GET: %s" % pformat(request.GET)
        if len(request.POST) > 0:
            print "POST: %s" % pformat(request.POST)
        if len(request.COOKIES) > 0:
            print "COOKIES: %s" % pformat(request.COOKIES)
        if len(request.FILES) > 0:
            print "FILES: %s" % pformat(request.FILES)

        if connection.queries:
            #print "-- %d SQL ---------" % len(connection.queries)
            for q in connection.queries:
                print 'SQL:%s || %s' % (q['time'], q['sql'])
        print
        return response



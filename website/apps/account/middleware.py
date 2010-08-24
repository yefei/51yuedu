# -*- coding: utf-8 -*-
# Create by: Yefe @ 2009-8-17
# $Id$
from time import mktime, time
from datetime import datetime
from website.apps.account.models import User, AnonymousUser, ONLINE_TIMEOUT
from website.apps.account.auth import get_user_from_authenticate_token, \
    AUTHENTICATE_SESSION_KEY, AUTHENTICATE_COOKIE_KEY


_LAST_REQUEST_AT_UPDATE_INTERVAL = 5 # 在线状态更新间隔
_ONLINE_CREDIT_TIME_SESSION_KEY = 'user_last_online_credit_at'

# 登陆认证
class AuthenticationMiddleware(object):
    def process_request(self, request):
        request.user = self.login_from_session(request) or self.login_from_cookie(request) or AnonymousUser()
        return None
    
    def process_response(self, request, response):
        if not hasattr(request, 'user'):
            return response
        # 如果用户已经退出或没认证 并且存在 login_cookie 则清除 login_cookie
        if not request.user.is_authenticated() and request.COOKIES.has_key(AUTHENTICATE_COOKIE_KEY):
            response.delete_cookie(AUTHENTICATE_COOKIE_KEY)
        return response
    
    def login_from_session(self, request):
        if request.session.has_key(AUTHENTICATE_SESSION_KEY):
            id = request.session[AUTHENTICATE_SESSION_KEY]
            try:
                return User.objects.get(pk=id)
            except User.DoesNotExist:
                del request.session[AUTHENTICATE_SESSION_KEY]
        return None
    
    def login_from_cookie(self, request):
        if request.COOKIES.has_key(AUTHENTICATE_COOKIE_KEY):
            user = get_user_from_authenticate_token(request.COOKIES[AUTHENTICATE_COOKIE_KEY])
            if user:
                request.session[AUTHENTICATE_SESSION_KEY] = user.id
                return user
        return None


# 用户状态更新
class StatusMiddleware(object):
    def process_request(self, request):
        if not hasattr(request, 'user'):
            return None
        u = request.user
        if u.is_authenticated():
            # 更新最后请求时间，在线时长
            diff = int(time() - mktime(u.last_request_at.timetuple()))
            if diff > _LAST_REQUEST_AT_UPDATE_INTERVAL:
                u.last_request_at = datetime.now()
                u.online_seconds += min(ONLINE_TIMEOUT, diff)
                User.objects.filter(pk=u.pk).update(
                    last_request_at = u.last_request_at,
                    online_seconds  = u.online_seconds
                )
            # /end
        return None


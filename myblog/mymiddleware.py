# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponseRedirect

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x


class SimpleMiddleware(MiddlewareMixin):
    '''没有登录不让访问'''

    def process_request(self, request):
        # print(request.path)
        path = request.path

        if path.find('/admin/password_change/') != -1:
            # 如果是demo 就重定向
            id = request.session['_auth_user_id']
            if id == '8':
                return HttpResponseRedirect('/no')

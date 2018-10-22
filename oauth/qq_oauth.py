from django.conf import settings
import requests
import os
from shortid import short_id
import re
import json

BASE_URL = 'https://graph.qq.com/oauth2.0/authorize'


def _get(url, params):
    r = requests.get(BASE_URL + url, params=params, headers={"Accept": 'application/json'})
    if (r.status_code == 200):
        return r.json()
    else:
        raise RuntimeError


# 获取认证url
def get_auth_url(request):
    domain = "https://" + request.META.get("HTTP_HOST")

    # 防止CSRF攻击
    state = short_id.get_short_id()

    client_id = __get_config('QQ_CLIENT_ID')
    redirect_uri = domain + __get_config('QQ_CLIENT_CALLBACK')
    request.session['state'] = state
    return BASE_URL + "?response_type=code&client_id={}&redirect_uri={}&state={}".format(client_id, redirect_uri, state)


def get_access_token(request, code):
    domain = "https://" + request.META.get("HTTP_HOST")

    url = 'https://graph.qq.com/oauth2.0/token?grant_type=authorization_code&client_id={}&client_secret={}&code={}&redirect_uri={}'.format(
        __get_config('QQ_CLIENT_ID'),
        __get_config('QQ_CLIENT_SECRET'),
        code,
        domain + __get_config('QQ_CLIENT_CALLBACK'))
    r = requests.get(url, headers={"Accept": 'application/json'})
    if (r.status_code == 200):
        str = r.text
        array = str.split("&")
        params = {}
        for item in array:
            items = item.split("=")
            params[items[0]] = items[1]
        return params
    else:
        raise RuntimeError(r.text)


# 获取用户信息
def get_user(access_token):
    rs = requests.get('https://graph.qq.com/oauth2.0/me?access_token={}'.format(access_token),
                      headers={"Accept": 'application/json'})
    if rs.status_code == 200:
        jsonp = rs.text
        p = re.match(r'callback\((.*?)\)', jsonp)
        if p:
            me = json.loads(p.group(1))
            openid = me.get('openid')
            params = {
                'access_token': access_token,
                'oauth_consumer_key': __get_config('QQ_CLIENT_ID'),
                'openid': openid
            }
            rs = requests.get('https://graph.qq.com/user/get_user_info', params=params,
                              headers={"Accept": 'application/json'})
            if rs.status_code == 200:
                user = rs.json()
                member = {}

                member['name'] = user.get('nickname')
                member['node_id'] = openid
                member['avatar_url'] = user.get('figureurl_qq_2')
                member['type'] = 1

                return member;
    pass


def __get_config(name):
    value = os.environ.get(name, getattr(settings, name, None))
    return value

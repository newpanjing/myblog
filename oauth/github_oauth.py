from django.conf import settings
import requests
import os
from shortid import short_id

BASE_URL = 'https://github.com'


def _get(url, params):
    r = requests.get(BASE_URL + url, params=params, headers={"Accept": 'application/json'})
    if (r.status_code == 200):
        return r.json()
    else:
        raise RuntimeError


def get_auth_url(request):
    domain = request.scheme + "://" + request.META.get("HTTP_HOST")
    clientId = __get_config("GITHUB_CLIENT_ID")
    redirect_uri = domain + __get_config("GITHUB_CLIENT_CALLBACK")
    state = short_id.get_short_id()
    request.session['state'] = state
    return BASE_URL + "/login/oauth/authorize?client_id=" + clientId + "&redirect_uri=" + redirect_uri + "&state=" + state


# 根据code 获取token
def get_access_token(request, code):
    domain = request.scheme + "://" + request.META.get("HTTP_HOST")
    clientId = __get_config("GITHUB_CLIENT_ID")
    client_secret = __get_config("GITHUB_CLIENT_SECRET")
    redirect_uri = domain + __get_config("GITHUB_CLIENT_CALLBACK")
    state = short_id.get_short_id()

    json = _get('/login/oauth/access_token', {
        "client_id": clientId,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
        "state": state
    })

    return json


# 根据token 获取用户
def get_user(access_token):
    r = requests.get('https://api.github.com/user', params={'access_token': access_token},
                     headers={"Accept": 'application/json'})

    if (r.status_code == 200):
        return r.json()
    else:
        raise RuntimeError


def __get_config(name):
    value = os.environ.get(name, getattr(settings, name, None))
    return value

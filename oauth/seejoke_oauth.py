import os

import requests
from django.conf import settings

BASE_URL = 'https://www.seejoke.com/service'


def get_auth_url(request):
    domain = request.scheme + "://" + request.META.get("HTTP_HOST")
    clientId = __get_config("SEEJOKE_CLIENT_ID")
    redirect_uri = domain + __get_config("SEEJOKE_CLIENT_CALLBACK")
    state = '88cto'
    return BASE_URL + "/auth2/auth?client_id=" + clientId + "&state=" + state + "&response_type=code" + "&redirect_uri=" + redirect_uri


# 根据token 获取用户
def get_user(token):
    clientId = __get_config("SEEJOKE_CLIENT_ID")
    secret = __get_config("SEEJOKE_CLIENT_SECRET")

    r = requests.get(BASE_URL + '/user',
                     params={
                         'client_id': clientId,
                         'secret': secret,
                         'state': '88cto',
                         'token': token
                     },
                     headers={"Accept": 'application/json'})

    if (r.status_code == 200):
        return r.json()
    else:
        raise RuntimeError


def __get_config(name):
    value = os.environ.get(name, getattr(settings, name, None))
    return value

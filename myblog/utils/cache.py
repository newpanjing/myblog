import redis
import os
import time
import datetime
import json
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# redis key命名参照alibaba规范

# 项目列表缓存
CACHE_PROJECT_KEY = 'cache:project'

# 通用数据
CACHE_COMMON_KEY = 'cache:common'

# 推荐
CACHE_RECOMMEND_KEY = 'cache:recommend'

# 首页缓存
CACHE_HOME_KEY = 'cache:home'


def _get_config(name):
    config = os.environ.get(name, getattr(settings, name, None))
    if config is not None:
        if isinstance(config, str):
            return config.strip()
        else:
            return config
    else:
        raise ImproperlyConfigured(
            "Can't find config for '%s' either in environment"
            "variable or in setting.py" % name)


con = redis.Redis(host=_get_config('REDIS_HOST'), port=_get_config('REDIS_PORT'))


def delete(key):
    print('删除缓存，key={}'.format(key))
    """
    删除缓存
    :param key: 
    :return: 
    """
    try:
        con.delete(key)
    except:
        print('删除缓存失败，key={}'.format(key))
        pass


def get(key, fun, timeout=None):
    """
    获取缓存
    :param key:
    :param fun: 回调方法
    :param timeout: 超时
    :return:
    """
    # begin = int(round(time.time() * 1000))
    value = None

    # 如果redis挂了 就不使用缓存
    try:
        value = con.get(key)

        if value:
            value = json.loads(value.decode(encoding="utf-8"))
        else:
            value = fun()
            str = json.dumps(value, cls=DateEncoder)
            if timeout:
                con.setex(key,timeout,str)
            else:
                con.set(key, str)
            print('缓存数据，key={}'.format(key))
            # end = int(round(time.time() * 1000))
        # print("time:{}ms".format(end - begin))
    except Exception as e:
        print(e)
        return fun()

    return value


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    print('ok')

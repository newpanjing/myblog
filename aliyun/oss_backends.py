from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import Storage
from oss2 import *
from django.conf import settings
import os
from shortid import short_id
from models.models import Config


def _get_db_config(group):
    dict = {}

    datas = Config.objects.filter(group=group)

    for i in datas:
        dict[i.key] = i.value
    return dict


class AliyunStorage(Storage):

    def __init__(self):
        config = _get_db_config('oss')

        self.access_key_id = config.get('key')
        self.access_key_secret = config.get('secret')
        self.endpoint = config.get('endpoint')
        self.bucket_name = config.get('bucket')
        self.cname = config.get('cname')

        self.auth = Auth(self.access_key_id, self.access_key_secret)
        self.bucket = self._get_bucket(self.auth)

    def _get_bucket(self, auth):
        # if self.cname:
        #     return Bucket(auth, self.cname, self.bucket_name, is_cname=True)
        # else:
        return Bucket(auth, self.endpoint, self.bucket_name)

    def _get_config(self, name):
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

    def exists(self, name):
        return self.bucket.object_exists(name)

    def url(self, name):
        # return self.bucket._make_url(self.bucket_name, name)
        return name

    def _save(self, name, content):
        # 为保证django行为的一致性，保存文件时，应该返回相对于`media path`的相对路径。

        # target_name = self._get_target_name(name)

        suffix = os.path.splitext(name)[1]
        target_name = short_id.get_short_id() + suffix
        content.open()
        content_str = b''.join(chunk for chunk in content.chunks())
        self.bucket.put_object(target_name, content_str)
        content.close()

        return self.cname + "/" + target_name

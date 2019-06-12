# -*- coding:utf-8 -*-
import os
import datetime
import json

from django.views import generic
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .configs import MDConfig

import base64
from shortid import short_id
from oss2 import *
from models.models import Config


def __get_db_config(group):
    dict = {}

    datas = Config.objects.filter(group=group).values('key', 'value')

    for i in datas:
        dict[i.get('key')] = i.get('value')
    return dict


# 初始化 oss
def get_oss_bucket():
    config = __get_db_config('oss')

    access_key_id = config.get('key')
    access_key_secret = config.get('secret')
    endpoint = config.get('endpoint')
    bucket_name = config.get('bucket')
    auth = Auth(access_key_id, access_key_secret)
    cname = config.get('cname')
    return {
        "bucket": Bucket(auth, endpoint, bucket_name),
        "cname": cname
    }


# TODO 此处获取default配置，当用户设置了其他配置时，此处无效，需要进一步完善
MDEDITOR_CONFIGS = MDConfig('default')


class UploadView(generic.View):
    """ upload image file """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UploadView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        upload_image = request.FILES.get("editormd-image-file", None)
        media_root = settings.MEDIA_ROOT

        # image none check
        if not upload_image:
            return HttpResponse(json.dumps({
                'success': 0,
                'message': "未获取到要上传的图片",
                'url': ""
            }))

        # image format check
        file_name_list = upload_image.name.split('.')
        file_extension = file_name_list.pop(-1)
        file_name = '.'.join(file_name_list)
        if file_extension not in MDEDITOR_CONFIGS['upload_image_formats']:
            return HttpResponse(json.dumps({
                'success': 0,
                'message': "上传图片格式错误，允许上传图片格式为：%s" % ','.join(
                    MDEDITOR_CONFIGS['upload_image_formats']),
                'url': ""
            }))

        suffix = os.path.splitext(upload_image._name)[1]
        target_name = short_id.get_short_id() + suffix
        rs = get_oss_bucket()
        rs.get('bucket').put_object(target_name, upload_image)

        url = rs.get('cname') + '/' + target_name

        return HttpResponse(json.dumps({'success': 1,
                                        'message': "上传成功！",
                                        'url': url}))

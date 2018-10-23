from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import json
import os
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


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER_CONFIG = {"imageActionName": "uploadimage", "imageFieldName": "upfile", "imageMaxSize": "2048000",
                 "imageAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"], "imageCompressEnable": "true",
                 "imageCompressBorder": "1600", "imageInsertAlign": "none", "imageUrlPrefix": "",
                 "imagePathFormat": "/ueditor/upload/image/{yyyy}{mm}{dd}/{time}{rand:6}",
                 "scrawlActionName": "uploadscrawl", "scrawlFieldName": "upfile",
                 "scrawlPathFormat": "/ueditor/upload/image/{yyyy}{mm}{dd}/{time}{rand:6}",
                 "scrawlMaxSize": "2048000", "scrawlUrlPrefix": "", "scrawlInsertAlign": "none",
                 "snapscreenActionName": "uploadimage",
                 "snapscreenPathFormat": "/ueditor/upload/image/{yyyy}{mm}{dd}/{time}{rand:6}",
                 "snapscreenUrlPrefix": "", "snapscreenInsertAlign": "none",
                 "catcherLocalDomain": ["127.0.0.1", "localhost", "img.baidu.com"], "catcherActionName": "catchimage",
                 "catcherFieldName": "source",
                 "catcherPathFormat": "/ueditor/upload/image/{yyyy}{mm}{dd}/{time}{rand:6}",
                 "catcherUrlPrefix": "", "catcherMaxSize": "2048000",
                 "catcherAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"], "videoActionName": "uploadvideo",
                 "videoFieldName": "upfile",
                 "videoPathFormat": "/ueditor/upload/video/{yyyy}{mm}{dd}/{time}{rand:6}", "videoUrlPrefix": "",
                 "videoMaxSize": "102400000",
                 "videoAllowFiles": [".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg", ".ogg", ".ogv",
                                     ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid"],
                 "fileActionName": "uploadfile", "fileFieldName": "upfile",
                 "filePathFormat": "/ueditor/upload/file/{yyyy}{mm}{dd}/{time}{rand:6}", "fileUrlPrefix": "",
                 "fileMaxSize": "51200000",
                 "fileAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".flv", ".swf", ".mkv", ".avi", ".rm",
                                    ".rmvb", ".mpeg", ".mpg", ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3",
                                    ".wav", ".mid", ".rar", ".zip", ".tar", ".gz", ".7z", ".bz2", ".cab", ".iso",
                                    ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md", ".xml"],
                 "imageManagerActionName": "listimage", "imageManagerListPath": "/ueditor/upload/image/",
                 "imageManagerListSize": "20", "imageManagerUrlPrefix": "", "imageManagerInsertAlign": "none",
                 "imageManagerAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
                 "fileManagerActionName": "listfile", "fileManagerListPath": "/ueditor/upload/file/",
                 "fileManagerUrlPrefix": "", "fileManagerListSize": "20",
                 "fileManagerAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".flv", ".swf", ".mkv", ".avi",
                                           ".rm", ".rmvb", ".mpeg", ".mpg", ".ogg", ".ogv", ".mov", ".wmv", ".mp4",
                                           ".webm", ".mp3", ".wav", ".mid", ".rar", ".zip", ".tar", ".gz", ".7z",
                                           ".bz2", ".cab", ".iso", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
                                           ".pdf", ".txt", ".md", ".xml"]}


def get_config():
    return HttpResponse(json.dumps(SERVER_CONFIG))


def upload_file(request):
    # 写入数据
    file = request.FILES.get("upfile")
    name = file.name
    suffix = os.path.splitext(name)[1]

    target_name = short_id.get_short_id() + suffix

    rs = get_oss_bucket()
    bucket = rs["bucket"]
    cname = rs["cname"]

    bucket.put_object(target_name, file)

    # 响应
    results = {
        "name": target_name,
        "original": target_name,
        "size": "",
        "state": "SUCCESS",
        "type": "png",
        "url": cname + "/" + target_name
    }

    return HttpResponse(json.dumps(results))


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


def upload_scrawl(request):
    # 涂鸦
    strs = request.POST.get("upfile")

    imgdata = base64.b64decode(strs)

    rs = get_oss_bucket()
    bucket = rs["bucket"]
    cname = rs["cname"]

    target_name = short_id.get_short_id() + ".png"
    bucket.put_object(target_name, imgdata)

    # 响应
    results = {
        "name": target_name,
        "original": target_name,
        "size": "",
        "state": "SUCCESS",
        "type": "png",
        "url": cname + "/" + target_name
    }

    return HttpResponse(json.dumps(results))


def handler(request):
    setattr(request, '_dont_enforce_csrf_checks', True)
    action = request.GET.get("action", "")
    if action == "config":
        return get_config()
    elif action == 'uploadscrawl':
        return upload_scrawl(request)
    else:
        return upload_file(request)

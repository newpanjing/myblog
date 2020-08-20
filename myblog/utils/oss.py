import oss2


def get_config(str):
    return {
        'key': '',
        'secret': '',
        'bucket': '',
        'endpoint': 'http://oss-cn-shenzhen.aliyuncs.com/',
        # 'endpoint': 'https://oss.88cto.com/',

    }


def put_object(file):
    oss_config = get_config('oss')

    key_id = oss_config['key']
    key_secret = oss_config['secret']
    bucket_name = oss_config['bucket']
    auth = oss2.Auth(key_id, key_secret)
    endpoint = oss_config['endpoint']
    bucket = oss2.Bucket(auth, endpoint, bucket_name)

    results = bucket.put_object('test.jpg', file)
    print(results)

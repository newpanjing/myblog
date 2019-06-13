from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
import os
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


def draw(text='', url=None, x=0, y=0, font_size=24, color='#FFF'):
    font = ImageFont.truetype(os.path.abspath(os.path.dirname(__file__)) + "/pingfang.ttf", font_size)

    r = requests.get(url, verify=False)
    # r = requests.get('http://oss.88cto.com/4y6MS8Rs.png')
    stream = BytesIO()
    stream.write(r.content)

    img1 = Image.open(stream)

    d = ImageDraw.Draw(img1)
    d.text((x, y), text, color, font=font)
    io_obj = BytesIO()
    # img1.save('/Users/panjing/Downloads/{}.png'.format(name))
    img1.save(io_obj, 'png')
    filename = short_id.get_short_id() + ".png"
    result = get_oss_bucket().get('bucket').put_object(filename, io_obj.getvalue())
    print(result)

    return get_oss_bucket().get('cname') + "/" + filename


if __name__ == '__main__':
    draw()

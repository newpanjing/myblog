import datetime
from django import template

register = template.Library()  # 这一句必须这样写

from article.models import Article
from article.models import Category
from models.models import Site
from models.models import Menu
from models.models import Notice
from models.models import Config

from ..utils import randoms


@register.simple_tag
def loadData():
    sites = Site.objects.all();
    categorys = Category.objects.all()
    menus = Menu.objects.all()
    notice = Notice.objects.last()
    recommeneds = getRecommend(10)

    configs = get_config('site')

    return {
        "sites": sites,
        "categorys": categorys,
        "menus": menus,
        "notice": notice,
        "recommeneds": recommeneds,
        'configs': configs
    }


def get_config(group):
    configs = Config.objects.filter(group=group)
    dicts = {}
    for c in configs:
        dicts[c.key] = c.value

    return dicts


def getRecommend(size):
    array = []
    count = Article.objects.count()
    indexs = randoms.getRandomArray(count, size)
    for i in indexs:
        obj = Article.objects.all()[i]
        array.append(obj)
    return array


@register.filter
def converToHtml(text):
    text = text.replace('\r\n', "<br/>")
    text = text.replace(' ', '&nbsp;')
    return text


@register.simple_tag
def get_now():
    return datetime.datetime.now()

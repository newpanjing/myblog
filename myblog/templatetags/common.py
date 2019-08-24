import datetime
from ..utils import pager
from django import template
import re
import json

register = template.Library()  # 这一句必须这样写

from article.models import Article
from article.models import Category
from models.models import Site
from models.models import Menu
from models.models import Notice
from models.models import Config

from ..utils import randoms
from ..utils import cache


def get_cache():
    return {
        'sites': list(Site.objects.order_by("sort").values('site', 'name')),
        'categorys': list(Category.objects.filter(display=True).order_by("sort").values('name', 'alias')),
        'menus': list(Menu.objects.filter(display=True).order_by('sort').values('name', 'icon', 'href')),
        'notice': Notice.objects.values('createDate', 'content').last(),
        'configs': get_config('site')
    }


def get_recommend():
    return getRecommend(5)


@register.simple_tag
def loadData():
    # redis缓存
    results = cache.get(cache.CACHE_COMMON_KEY, get_cache)
    # 推荐5分钟更新一次，其余的永久缓存，有更新的时候刷新缓存
    results['recommeneds'] = cache.get(cache.CACHE_RECOMMEND_KEY, get_recommend, 300)
    return results


def get_config(group):
    configs = Config.objects.filter(group=group).values('key', 'value')
    dicts = {}
    for c in configs:
        dicts[c.get('key')] = c.get('value')

    return dicts


def getRecommend(size):
    array = []
    count = Article.objects.filter(image__isnull=False).exclude(image='').count()
    if count == 0:
        return array

    indexs = randoms.getRandomArray(count, size)
    for i in indexs:
        obj = \
            Article.objects.filter(image__isnull=False).exclude(image='').values('title', 'sid', 'image',
                                                                                 'category__name',
                                                                                 'category__alias',
                                                                                 'createDate')[i]
        array.append(obj)
    return array


@register.filter
def url(url):
    u = str(url)
    if u.find('http') != 0:
        u = "/" + u
    return u


@register.filter
def filter(url):
    if url:
        return url
    else:
        return 'javascript:;'


@register.filter
def converToHtml(text):
    text = text.replace('\r\n', "<br/>")
    text = text.replace(' ', '')
    return text


@register.filter
def clear(text):
    p = re.compile(r'([&]{0,1}(\w+;))')
    text = re.sub(p, '', text)
    p = re.compile(r'\r|\n|\t|\s')
    text = re.sub(p, '', text)
    return text


@register.simple_tag
def get_now():
    return datetime.datetime.now()


@register.simple_tag(takes_context=True)
def get_pager(context):
    total = context["total"]

    current = context["current"]
    current = int(current)

    url = context["url"]

    size = int(context["size"])
    show_number = int(context["show_number"])

    total_page_num = int((total - 1) / size + 1)
    if total_page_num < 2:
        return ""

    array = pager.get_numbers(total, size, current, show_number)
    buffer = []
    buffer.append('<div class="pager-block"><nav><ul class="pagination">')
    prev = ''
    href = url + '/' + str(current - 1)
    if current <= 1:
        prev = 'class="disabled"'
        href = 'javascript:;'
    buffer.append('<li ' + prev + '><a href="' + href + '" aria-label="Previous">上一页</a></li>')

    for i in array:
        page = str(i)
        active = ''
        if current == i:
            active = 'class="active"'
        buffer.append(' <li ' + active + '><a href="' + url + '/' + page + '">' + page + '</a></li>')

    next = ''
    href = url + '/' + str(current + 1)
    if current == total_page_num:
        next = 'class="disabled"'
        href = 'javascript:;'

    buffer.append(
        '<li ' + next + '><a href="' + href + '" aria-label="Next">下一页</a></li></ul></nav></div>')
    return ''.join(buffer)

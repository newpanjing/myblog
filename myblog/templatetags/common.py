import datetime
from ..utils import pager
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
    menus = Menu.objects.filter(display=True)
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
def url(url):
    u = str(url)
    if u.find('http') != 0:
        u = "/" + u
    return u


@register.filter
def converToHtml(text):
    text = text.replace('\r\n', "<br/>")
    text = text.replace(' ', '')
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

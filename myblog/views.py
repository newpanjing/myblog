from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from article.models import Article
from article.models import Category
from models.models import Page
import re
import datetime
from django.http import Http404


# 主页
def home(request):
    tops = Article.objects.filter(top=True).order_by('-id')
    # p = Paginator(datas, 10)
    # page = request.GET.get('page')
    # if page is None:
    #     page = 1
    # articles = p.page(page)

    articles = Article.objects.filter(top=False).order_by("-id")[:10]

    return render(request, 'index.html', {
        "tops": tops,
        "articles": articles
    })


# 文章详情
def detail(request, id):
    # 查询一条数据
    article = None
    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        raise Http404

    # 修改点击量
    article.hits += 1
    article.save()

    return render(request, "detail.html", {
        'id': id,
        'article': article
    })


# 所有分类
def category_all(request):
    return category(request, None)


# 单个分类
def category(request, alias):
    return category_page(request, alias, 1)


# 分类分页
def category_page(request, alias, page):
    category = None

    suffix = ''
    if alias:
        # 如果全是数字，就是分页，不是就是别名
        suffix = "/" + alias
        mathchObj = re.match(r'\d+', alias, flags=0)
        if mathchObj:
            page = alias
            suffix = ''
        else:
            category = Category.objects.get(alias=alias)

    filter = {}
    if category:
        filter["category"] = category.id

    count = Article.objects.filter(**filter).count()
    articles = Article.objects.filter(**filter).order_by("-id")

    size = 10
    show = 10

    paginator = Paginator(articles, size)
    articles = paginator.page(page)

    return render(request, 'category.html', {
        "cdata": category,
        "articles": articles,
        "total": count,
        "current": page,
        "url": '/category' + suffix,
        "size": size,
        "show_number": show
    })


# 自定义页面
def page(request, alias):
    page = Page.objects.get(alias=alias)
    return render(request, 'page.html', {
        "page": page
    })


# sitemap
def sitemap(request):
    list = Article.objects.all().order_by("-id")
    domain = request.scheme + "://" + request.META.get("HTTP_HOST")
    buffer = []
    buffer.append('<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<urlset>\n')

    for article in list:
        buffer.append('<url>\n')
        buffer.append('<loc>{domain}/article/{article.id}</loc>\n'.format(domain=domain, article=article))
        buffer.append('<priority>0.8</priority>\n')
        buffer.append('<lastmod>{date}</lastmod>\n'.format(date=datetime.datetime.now().strftime('%Y-%m-%d')))
        buffer.append('<changefreq>daily</changefreq>\n')
        buffer.append('</url>\n')

    buffer.append('</urlset>')
    return HttpResponse(content=buffer, content_type="application/xml")


# 500 错误
def page_error(request):
    params = {}
    if request.path.find("500") != -1:
        params["code"] = "500"
        params['msg'] = "服务器内部错误，请稍后重试！"
    else:
        params["code"] = "404"
        params['msg'] = "抱歉，该页面没有找到！"
    return render(request, 'error.html', params)

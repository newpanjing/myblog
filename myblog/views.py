from django.core.paginator import Paginator
from django.shortcuts import render
from article.models import Article
from article.models import Category


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


def detail(request, id):
    # 查询一条数据
    article = Article.objects.get(id=id)

    # 修改点击量
    article.hits += 1
    article.save()

    return render(request, "detail.html", {
        'id': id,
        'article': article
    })


def categoryAll(request):
    return render(request, 'category.html')


def category(request, id):
    return category_page(request, id, 1)


def category_page(request, id, page):
    category = Category.objects.get(id=id)

    count = Category.objects.filter(id=id).count()
    articles = Article.objects.filter(category=id)

    paginator = Paginator(articles, 20)
    articles = paginator.page(page)

    return render(request, 'category.html', {
        "cdata": category,
        "articles": articles,
        "count": count
    })

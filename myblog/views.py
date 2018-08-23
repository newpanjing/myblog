from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from article.models import Article
from article.models import Category
from models.models import Page
from article.models import Member
from article.models import Comment
import re
import datetime
from django.http import Http404
from github import oauth
from django.http import HttpResponseRedirect
from shortid import short_id
import json
from django.forms.models import model_to_dict


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

    sid = short_id.get_short_id()
    request.session['sid'] = sid

    # 查询评论
    comment = get_comment(0, id)

    return render(request, "detail.html", {
        'id': id,
        'article': article,
        'sid': sid,
        'comment': comment
    })


# 所有分类
def category_all(request):
    return category(request, None)


# 单个分类
def category(request, alias):
    return category_page(request, alias, 1)


# 获取评论
def get_comment(type, targetId):
    # 参与人数
    people = Comment.objects.filter(type=type, targetId=targetId, parentId__isnull=True).count()
    # 评论条数
    count = Comment.objects.filter(type=type, targetId=targetId).count()

    # 查询评论list
    list = Comment.objects.filter(type=type, targetId=targetId, parentId__isnull=True).order_by("-id")
    # 分页待处理
    for item in list:
        item.comments = Comment.objects.filter(parentId=item.id).order_by("-id")

    return {
        'people': people,
        'count': count,
        'list': list
    }


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

    sid = short_id.get_short_id()
    request.session['sid'] = sid
    comment = get_comment(2, page.id)
    return render(request, 'page.html', {
        "page": page,
        "sid": sid,
        "comment": comment
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


# GitHub登录
def oauth_github(request):
    url = oauth.get_auth_url(request)
    # 记录来源页
    if 'HTTP_REFERER' in request.META:
        referer = request.META['HTTP_REFERER']
        request.session['referer'] = referer

    return HttpResponseRedirect(url)


# Github登录回调
def oauth_github_callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")
    # 如果 state和session中的不一致，可能是伪造的请求
    if request.session['state'] != state:
        return HttpResponse('参数校验不通过，疑是非法请求。')

    rs = oauth.get_access_token(request, code)

    user = oauth.get_user(rs['access_token'])

    member = None
    # 跳转到来源页
    # 数据库更新用户信息
    try:
        member = Member.objects.filter(nodeId=user["node_id"]).get()
        member.name = user['name']
        member.avatar = user['avatar_url']
        member.blog = user['blog']
        member.url = user['html_url']
        member.email = user['email']
        member.nodeId = user['node_id']
        member.save()
    except:
        member = Member.objects.create(
            name=user['name'],
            avatar=user['avatar_url'],
            blog=user['blog'],
            url=user['html_url'],
            email=user['email'],
            nodeId=user['node_id'],
        )
    request.session['member'] = model_to_dict(member)

    url = '/'
    referer = request.session['referer']
    if referer:
        url = referer
    return HttpResponseRedirect(url)


# 保存评论
def comments_save(request):
    # 通过session限制评论频率

    result = {}
    session = request.session;
    post = request.POST;
    ssid = session['sid']

    sid = post.get('SID')
    targetId = post.get('TARGET_ID')
    parentId = post.get('parentId')

    member = session['member']

    dbMember = Member.objects.get(id=member['id'])

    atMemberId = post.get('atMemberId')
    type = post.get('type')
    if type is None:
        type = 0

    if ssid != sid:
        result = {
            'code': 0,
            'msg': '非法请求'
        }
    elif member is None:
        result = {
            'code': 0,
            'msg': '用户未登录'
        }
    else:
        obj = Comment.objects.create(
            member=dbMember,
            content=post.get('content'),
            type=type,
            targetId=targetId,
            parentId=parentId,
            atMember_id=atMemberId
        )
        result = {
            'code': 1,
            'msg': '评论成功',
            'id': obj.id
        }

        return HttpResponse(json.dumps(result), content_type="application/json")

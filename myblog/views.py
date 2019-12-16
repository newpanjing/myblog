from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from article.models import Article
from article.models import Category
from models.models import Page
from article.models import Member
from article.models import Comment
import datetime
from django.http import Http404
from oauth import github_oauth
from oauth import qq_oauth
from oauth import seejoke_oauth

from django.http import HttpResponseRedirect
from shortid import short_id
import json
from django.forms.models import model_to_dict

from .utils import randoms
import requests
import markdown
from jieba import analyse
import random
from .utils import cache


def __get_home_data():
    fields = ('sid', 'image', 'title', 'subject', 'createDate', 'hits', 'category__alias', 'category__name')
    return {
        "tops": list(Article.objects.filter(top=True).order_by('-id').values(*fields)),
        "articles": list(Article.objects.filter(top=False).order_by("-id").values(*fields)[:10])
    }


# 主页
def home(request):
    data = cache.get(cache.CACHE_HOME_KEY, __get_home_data)
    return render(request, 'index.html', data)


# 文章详情
def detail(request, id):
    query_set = {}
    # 如果是数字就是id，不是就是sid
    if id.isdigit():
        query_set["id"] = id
    else:
        query_set["sid"] = id

    # 查询一条数据
    article = None
    try:
        article = Article.objects.get(**query_set)

    except Article.DoesNotExist:
        raise Http404

    # 修改点击量
    article.hits += 1
    article.save()

    # 如果是markdown，就用markdown渲染
    article.content = '[TOC]\n' + article.content
    article.content = markdown.markdown(article.content, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])

    if '[TOC]' in article.content:
        article.content = article.content.replace('[TOC]', '')

    sid = short_id.get_short_id()
    request.session['sid'] = sid

    # 查询评论
    comment = get_comment(0, article.id)

    # 随机10片文章
    recommends = get_recommend(10)

    return render(request, "detail.html", {
        'id': id,
        'article': article,
        'sid': sid,
        'comment': comment,
        'recommends': recommends
    })


def get_recommend(size):
    array = []
    count = Article.objects.count()
    if count == 0:
        return array

    indexs = randoms.getRandomArray(count, size)
    for i in indexs:
        obj = Article.objects.all().values('title', 'sid')[i]
        array.append(obj)
    return array


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
        if alias.isdigit():
            page = alias
            suffix = ''
        else:
            category = Category.objects.values('id', 'name').get(alias=alias)

    filter = {}
    if category:
        filter["category"] = category.get('id')

    count = Article.objects.filter(**filter).count()
    articles = Article.objects.filter(**filter).values('image', 'category__alias', 'category__name', 'sid',
                                                       'title', 'subject', 'createDate', 'hits').order_by("-id")

    size = 10
    show = 5

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
    page = Page.objects.values('title', 'content', 'id').get(alias=alias)
    page['content'] = markdown.markdown(page.get('content'), extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ], safe_mode=True, enable_attributes=False)
    sid = short_id.get_short_id()
    request.session['sid'] = sid
    comment = get_comment(2, page.get('id'))
    return render(request, 'page.html', {
        "page": page,
        "sid": sid,
        "comment": comment
    })


# sitemap
def sitemap(request):
    list = Article.objects.values('sid').all().order_by("-id")
    domain = request.scheme + "://" + request.META.get("HTTP_HOST")

    buffer = []
    buffer.append(
        '<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<urlset  xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\nxmlns:mobile="http://www.baidu.com/schemas/sitemap-mobile/1/">\n')

    # 分类页面

    categorys = Category.objects.all().values('alias').order_by("sort")
    for category in categorys:
        buffer.append("<url>\n")
        buffer.append('<loc>{domain}/category/{alias}</loc>\n'.format(domain=domain, alias=category.get('alias')))
        buffer.append('<mobile:mobile type="pc,mobile"/>')
        buffer.append('<priority>0.8</priority>\n')
        buffer.append('<lastmod>{date}</lastmod>\n'.format(date=datetime.datetime.now().strftime('%Y-%m-%d')))
        buffer.append('<changefreq>daily</changefreq>\n')
        buffer.append('</url>\n')

    pages = Page.objects.values('alias').all()
    for page in pages:
        buffer.append("<url>\n")
        buffer.append('<loc>{domain}/page/{alias}</loc>\n'.format(domain=domain, alias=page.get('alias')))
        buffer.append('<mobile:mobile type="pc,mobile"/>')
        buffer.append('<priority>0.8</priority>\n')
        buffer.append('<lastmod>{date}</lastmod>\n'.format(date=datetime.datetime.now().strftime('%Y-%m-%d')))
        buffer.append('<changefreq>daily</changefreq>\n')
        buffer.append('</url>\n')

    for article in list:
        buffer.append('<url>\n')
        buffer.append('<loc>{domain}/article/{sid}</loc>\n'.format(domain=domain, sid=article.get('sid')))
        buffer.append('<mobile:mobile type="pc,mobile"/>')
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
    url = github_oauth.get_auth_url(request)
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

    rs = github_oauth.get_access_token(request, code)

    user = github_oauth.get_user(rs['access_token'])
    user['type'] = 0
    # 处理用户
    return update_user(request, user)


def update_user(request, user):
    member = None
    # 跳转到来源页
    # 数据库更新用户信息
    try:
        member = Member.objects.filter(nodeId=user.get("node_id")).get()
        # 没有名字，取登录名
        if user.get('name') is None:
            member.name = user.get('login')
        else:
            member.name = user.get('name')

        member.avatar = user.get('avatar_url')
        member.blog = user.get('blog')
        member.url = user.get('html_url')
        member.email = user.get('email')
        member.nodeId = user.get('node_id')
        member.type = user.get('type')
        member.save()
    except:
        member = Member.objects.create(
            name=user.get('name'),
            avatar=user.get('avatar_url'),
            blog=user.get('blog'),
            url=user.get('html_url'),
            email=user.get('email'),
            nodeId=user.get('node_id'),
            type=user.get('type')
        )

    if member.url is None:
        member.url = 'javascript:;'
    request.session['member'] = model_to_dict(member)

    url = '/'
    referer = request.session['referer']
    if referer:
        url = referer
        # 如果是logout 就跳转首页
        if url.find('logout') != -1:
            url = '/'
    return HttpResponseRedirect(url)


# QQ登录
def oauth_qq(request):
    url = qq_oauth.get_auth_url(request)
    # 记录来源页
    if 'HTTP_REFERER' in request.META:
        referer = request.META['HTTP_REFERER']
        request.session['referer'] = referer

    return HttpResponseRedirect(url)


def oauth_qq_callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")
    # 如果 state和session中的不一致，可能是伪造的请求
    if request.session['state'] != state:
        return HttpResponse('参数校验不通过，疑是非法请求。')
    rs = qq_oauth.get_access_token(request, code)
    access_token = rs.get('access_token')
    user = qq_oauth.get_user(access_token)

    # 处理用户
    return update_user(request, user)


def oauth_seejoke(request):
    url = seejoke_oauth.get_auth_url(request)
    # 记录来源页
    if 'HTTP_REFERER' in request.META:
        referer = request.META['HTTP_REFERER']
        request.session['referer'] = referer

    return HttpResponseRedirect(url)


def oauth_seejoke_callback(request):
    token = request.GET.get("token")

    rs = seejoke_oauth.get_user(token)

    user = {}

    if (rs.get('code') == 0):
        data = rs.get('data')

        user['name'] = data.get('userName')
        user['email'] = data.get('email')
        user['node_id'] = data.get('id')
        user['avatar_url'] = data.get('head')
        user['url'] = data.get('address')
        user['type'] = 2

    # 处理用户
    return update_user(request, user)


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


def __get_project():
    r = requests.get("https://api.github.com/users/newpanjing/repos?sort=updated&direction=desc")
    if r.status_code == 200:
        return r.json()
    else:
        raise RuntimeError(r.text)


def project(request):
    # 缓存时间为12小时 43200
    rs = cache.get(cache.CACHE_PROJECT_KEY, __get_project, 43200)
    return render(request, 'project.html', {
        'rs': rs
    })


def project_detail(request, name):
    r = requests.get("https://api.github.com/repos/newpanjing/{}".format(name))
    rs = None
    readme = None
    tags = None
    if r.status_code == 200:
        rs = r.json()
        # 读取 readme
        if rs["description"]:
            arry = analyse.extract_tags(rs["description"], topK=5)
            tags = ','.join(arry)

        r = requests.get("https://raw.githubusercontent.com/newpanjing/{}/master/README.md?_={}".format(name,
                                                                                                        random.uniform(
                                                                                                            100, 999)))
        if r.status_code == 200:
            readme = markdown.markdown(r.text)

    sid = short_id.get_short_id()
    request.session['sid'] = sid
    comment = get_comment(3, name)

    return render(request, 'project_detail.html', {
        'item': rs,
        'readme': readme,
        'name': name,
        'tags': tags,
        "sid": sid,
        "comment": comment
    })


def logout(request):
    if request.session.get('member'):
        del request.session['member']

    return render(request, 'logout.html')


def no(request):
    return render(request, 'no.html')


def simplepro_info(request):
    return render(request, 'admin/tips.html')

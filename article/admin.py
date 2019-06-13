import random

from django.contrib import admin

from .models import *
import re

from myblog.utils import oss
from jieba import analyse
from shortid import short_id
from myblog.utils import cache
from draw import draw


# Register your models here.
# 获取简介
def get_subject(html):
    # 移除style标签和script标签

    regexs = [r'([&]{0,1}(\w+;))',
              r'\r|\n|\t|\s'
              r'<script>.*?</script>',
              r'<style.*?</style>',
              r'<[^>]+>'
              ]

    for r in regexs:
        p = re.compile(r)
        html = re.sub(p, '', html)

    return html


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'alias', 'date', 'sort', 'display')
    list_display_links = ('id', 'name', 'alias')
    search_fields = ('name',)
    list_editable = ('display', 'sort')

    def save_model(self, request, obj, form, change):
        super(CategoryAdmin, self).save_model(request, obj, form, change)
        cache.delete(cache.CACHE_COMMON_KEY)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'sid', 'title_url', 'comment_count', 'category', 'user', 'hits', 'tags', 'top', 'createDate')
    list_filter = ('createDate', 'category', 'user', 'title')
    search_fields = ('title',)
    list_display_links = ('id', 'sid', 'title_url')
    list_editable = ('top', 'category')
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        subject = get_subject(obj.content)
        # oss.put_object(obj.image.file.file)
        # 不超过200字
        if len(subject) > 200:
            subject = subject[0:200]

        # 短id
        if not obj.sid:
            obj.sid = short_id.get_short_id()

        obj.subject = subject
        # 处理标签
        tags = obj.tags
        # 自动生成
        if tags is None or tags is "":
            r = analyse.extract_tags(subject, topK=5)
            tags = ",".join(r)

        obj.tags = tags

        # 如果没有封面就生成
        if obj.image == '':
            total = Cover.objects.count()
            c = Cover.objects.all()[random.randint(0, total - 1)]
            url = draw.draw(text=obj.title, url=c.image.url, font_size=c.font_size, color=c.color, x=c.x, y=c.y)
            obj.image.name = url
        super(ArticleAdmin, self).save_model(request, obj, form, change)
        cache.delete(cache.CACHE_HOME_KEY)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        'id', 'name', 'email', 'nodeId', 'type', 'avatar_img', 'github_url', 'blog_url', 'createDate', 'updateDate')
    list_display_links = ('id', 'name', 'email', 'nodeId', 'createDate', 'updateDate')
    search_fields = ('name', 'email',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'show_content', 'member', 'atMember', 'parentId', 'targetId', 'createDate')
    list_per_page = 10
    list_filter = ('member', 'type')
    search_fields = ('content',)


@admin.register(Cover)
class CoverAdmin(admin.ModelAdmin):
    list_display = ('id', 'x', 'y', 'font_size', 'color_display', 'image_display')
    list_per_page = 20
    list_editable = ('x', 'y', 'font_size')

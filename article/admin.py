from django.contrib import admin

from .models import *
import re

from myblog.utils import oss
from jieba import analyse
from shortid import short_id


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


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'sid', 'title_url', 'comment_count', 'category', 'user', 'hits', 'tags', 'top', 'createDate')
    list_filter = ('category', 'user')
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
        obj.sid = short_id.get_short_id()

        obj.subject = subject
        # 处理标签
        tags = obj.tags
        # 自动生成
        if tags is None or tags is "":
            r = analyse.extract_tags(subject, topK=5)
            tags = ",".join(r)

        obj.tags = tags
        super(ArticleAdmin, self).save_model(request, obj, form, change)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'email', 'nodeId', 'type', 'avatar_img', 'github_url', 'blog_url', 'createDate', 'updateDate')
    list_display_links = ('id', 'name', 'email', 'nodeId', 'createDate', 'updateDate')
    search_fields = ('name', 'email',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'content', 'member', 'atMember', 'parentId', 'targetId', 'createDate')
    list_per_page = 10
    list_filter = ('member', 'type')
    search_fields = ('content',)

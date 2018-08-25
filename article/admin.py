from django.contrib import admin

from .models import *
import re

from myblog.utils import oss


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
    list_display = ('id', 'name', 'alias', 'date')
    list_display_links = ('id', 'name', 'alias')
    search_fields = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_url', 'category', 'user', 'hits', 'tags', 'createDate')
    list_filter = ('category', 'user')
    search_fields = ('title_url',)
    list_display_links = ('id', 'title_url')

    list_per_page = 10

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        subject = get_subject(obj.content)
        # oss.put_object(obj.image.file.file)
        # 不超过200字
        if len(subject) > 200:
            subject = subject[0:200]

        obj.subject = subject
        super(ArticleAdmin, self).save_model(request, obj, form, change)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'nodeId', 'avatar_img', 'github_url', 'blog_url', 'createDate', 'updateDate')
    list_display_links = ('id', 'name', 'email', 'nodeId', 'createDate', 'updateDate')
    search_fields = ('name', 'email')



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'content', 'member', 'atMember', 'parentId', 'targetId', 'createDate')
    list_per_page = 10

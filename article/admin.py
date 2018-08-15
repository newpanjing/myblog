from django.contrib import admin

from .models import *
import re

from myblog.utils import oss


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'alias', 'date')
    list_display_links = ('id', 'name', 'alias')
    search_fields = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'user', 'hits', 'tags', 'createDate')
    list_filter = ('category', 'user')
    search_fields = ('title',)
    list_display_links = ('id', 'title')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        subject = getSubject(obj.content)
        # oss.put_object(obj.image.file.file)
        # 不超过200字
        if len(subject) > 200:
            subject = subject[0:200]

        obj.subject = subject
        super(ArticleAdmin, self).save_model(request, obj, form, change)


# 获取简介
def getSubject(html):
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

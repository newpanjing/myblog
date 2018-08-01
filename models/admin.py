from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    """
    系统配置
    """
    list_display = ('id', 'group', 'key', 'value')
    search_fields = ('group', 'key')
    list_filter = ('group',)


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'site', 'contact', 'contactType', 'createDate')
    search_fields = ('contactType',)
    list_filter = ('contactType',)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'alias', 'title', 'keywords', 'description', 'createDate', 'display')
    search_fields = ('title', 'alias')
    list_filter = ('display',)
    list_display_links = ('id', 'alias', 'title')


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon', 'href', "display")
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'createDate')
    search_fields = ('title',)
    list_display_links = ('title',)

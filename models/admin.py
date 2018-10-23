from django.contrib import admin
from .models import *

from myblog.utils import cache


# Register your models here.

@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    """
    系统配置
    """
    list_display = ('id', 'group', 'key', 'value')
    search_fields = ('group', 'key')
    list_filter = ('group',)
    list_display_links = ('id', 'group', 'key', 'value')

    def save_model(self, request, obj, form, change):
        super(ConfigAdmin, self).save_model(request, obj, form, change)
        cache.delete(cache.CACHE_COMMON_KEY)


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'site', 'contact', 'contactType', 'sort', 'createDate')
    search_fields = ('contactType',)
    list_filter = ('contactType',)
    list_display_links = ('id', 'name', 'site')
    list_editable = ('sort',)

    def save_model(self, request, obj, form, change):
        super(SiteAdmin, self).save_model(request, obj, form, change)
        cache.delete(cache.CACHE_COMMON_KEY)


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
    list_editable = ('display',)

    def save_model(self, request, obj, form, change):
        super(MenuAdmin, self).save_model(request, obj, form, change)
        cache.delete(cache.CACHE_COMMON_KEY)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'createDate')
    search_fields = ('title',)
    list_display_links = ('title',)

    def save_model(self, request, obj, form, change):
        super(NoticeAdmin, self).save_model(request, obj, form, change)
        cache.delete(cache.CACHE_COMMON_KEY)

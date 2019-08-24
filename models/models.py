from django.db import models
from mdeditor.fields import MDTextField


# Create your models here.

class Config(models.Model):
    key = models.CharField(max_length=128, db_index=True)
    value = models.CharField(max_length=512)
    group = models.CharField(max_length=128, verbose_name='组', db_index=True)

    class Meta:
        verbose_name = "字典列表"
        verbose_name_plural = "字典列表"
        # app_label = "config"

    def __str__(self):
        return self.group + '.' + self.key


class Site(models.Model):
    site = models.CharField(max_length=256, verbose_name='网址')
    name = models.CharField(max_length=128, verbose_name='名称')
    contact_choices = ((0, 'QQ'),
                       (1, '微信'),
                       (2, '邮箱'),
                       (3, '手机')
                       )
    contactType = models.IntegerField(choices=contact_choices, verbose_name='类型', default=0)
    contact = models.CharField(max_length=128, verbose_name='联系方式')
    createDate = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    sort = models.IntegerField(verbose_name='排序', default=0, null=True, blank=True, db_index=True)

    class Meta:
        verbose_name = "友链"
        verbose_name_plural = "友链管理"

    def __str__(self):
        return self.name


class Page(models.Model):
    alias = models.CharField(max_length=256, verbose_name='别名', db_index=True)
    title = models.CharField(max_length=256, verbose_name='标题')
    keywords = models.CharField(max_length=512, verbose_name='关键字', null=True, blank=True)
    description = models.CharField(max_length=512, verbose_name='描述', null=True, blank=True)
    content = MDTextField(verbose_name='内容')
    createDate = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    display = models.BooleanField(verbose_name='是否显示', default=True, db_index=True)
    head = models.TextField(verbose_name='头部脚本', null=True, blank=True)
    footer = models.TextField(verbose_name='尾部脚本', null=True, blank=True)

    class Meta:
        verbose_name = '页面'
        verbose_name_plural = '页面管理'

    def __str__(self):
        return self.title


class Menu(models.Model):
    name = models.CharField(max_length=16, verbose_name='菜单名')
    icon = models.CharField(max_length=32, verbose_name='图标字体', null=True, blank=True)
    href = models.CharField(max_length=128, verbose_name='链接地址')
    createDate = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    display = models.BooleanField(verbose_name='显示', default=True, db_index=True)
    sort = models.IntegerField(verbose_name='排序', default=0, db_index=True)

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = '菜单管理'

    def __str__(self):
        return self.name


class Notice(models.Model):
    title = models.CharField(max_length=128, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    createDate = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告管理'

    def __str__(self):
        return self.title

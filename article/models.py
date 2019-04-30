from django.db import models
from django.contrib.auth.models import User
# from ckeditor.fields import RichTextField
from ueditor.fields import RichTextField
from django.utils.html import format_html


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, verbose_name='分类名', blank=False, null=False)
    alias = models.CharField(max_length=128, verbose_name='别名', db_index=True)
    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    display = models.BooleanField(verbose_name='显示', default=True, db_index=True)
    sort = models.IntegerField(verbose_name='排序', default=0, db_index=True)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类管理"

    def __str__(self):
        return self.name


class Article(models.Model):
    sid = models.CharField(max_length=8, verbose_name='短ID', blank=True, null=True, editable=False, db_index=True)
    title = models.CharField(max_length=256, verbose_name='标题', blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=False, null=True, verbose_name='分类',
                                 db_index=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='发布者', null=True, editable=False)
    hits = models.IntegerField(verbose_name='点击量', default=0, editable=False)
    content = RichTextField(verbose_name='内容', null=False, blank=False, config={})
    subject = models.TextField(verbose_name='简介', editable=False)
    image = models.ImageField(upload_to='static/images/', verbose_name='封面', blank=True, null=True, db_index=True)
    createDate = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    tags = models.CharField(max_length=256, verbose_name='标签', blank=True, null=True)
    top_choices = ((0, '否'),
                   (1, '是'),)
    top = models.IntegerField(choices=top_choices, verbose_name='置顶', default=0, db_index=True)

    def comment_count(self):
        return Comment.objects.filter(targetId=self.id, type=0).count()

    def title_url(self):
        return format_html('<a href="/article/{}" target="_blank">{}</a>', self.sid, self.title)

    title_url.short_description = "标题"
    comment_count.short_description = "评论数"

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章管理"

    def __str__(self):
        return self.title


class Member(models.Model):
    name = models.CharField(max_length=128, verbose_name='昵称', blank=True, null=False, default='no_name')
    email = models.CharField(max_length=256, verbose_name='邮箱', blank=True, null=True)
    nodeId = models.CharField(max_length=256, verbose_name='OAuth ID', blank=False, null=False)
    avatar = models.CharField(max_length=256, verbose_name='头像', null=False, blank=False)
    url = models.CharField(max_length=256, verbose_name='主页', blank=True, null=True)
    blog = models.CharField(max_length=256, verbose_name='博客', blank=True, null=True)
    createDate = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    updateDate = models.DateTimeField(verbose_name='更新日期', auto_now=True)
    type_choices = (
        (0, 'Github'),
        (1, 'QQ'),
        (2, '代码集市')
    )
    type = models.IntegerField(choices=type_choices, verbose_name='用户类型', db_index=True)

    def github_url(self):
        if self.url is None:
            return ""
        else:
            return format_html('<a href="{}" target="_blank">{}</a>', self.url, self.url)

    def avatar_img(self):
        return format_html('<img src="{}" style="width:25px;height:25px"/>', self.avatar)

    def blog_url(self):
        if self.blog is None or self.blog == "":
            return ""
        else:
            url = self.blog
            if url.find("http") != 0:
                url = "http://" + url
            return format_html('<a href="{}" target="_blank">{}</a>', url, url)

    avatar_img.short_description = "头像"
    blog_url.short_description = "博客"

    def __str__(self):
        if self.name:
            return self.name
        else:
            return '-'

    class Meta:
        verbose_name = "会员"
        verbose_name_plural = "会员管理"


class Comment(models.Model):
    content = models.TextField(verbose_name='内容', null=False, blank=True)

    member = models.ForeignKey(Member, on_delete=models.SET_NULL, verbose_name='用户', null=True, editable=False,
                               db_index=True)
    parentId = models.IntegerField(verbose_name='父ID', null=True, blank=True, db_index=True)
    targetId = models.CharField(max_length=128, db_index=True, verbose_name='目标ID', null=True, blank=True)
    type_choices = ((0, '文章'),
                    (1, '留言'),
                    (2, '页面'),
                    (3, '项目'),)
    type = models.IntegerField(choices=type_choices, verbose_name='类型', db_index=True)
    createDate = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    atMember = models.ForeignKey(Member, related_name='at_member_id', on_delete=models.SET_NULL, verbose_name='回复用户',
                                 null=True, blank=True,
                                 editable=False, db_index=True)

    def show_content(self):
        url = ''
        if type == 0:
            url = '/article/' + str(self.targetId)
        elif type == 1:
            url = '/page/message/#' + str(self.targetId)
        else:
            url = 'javascript:;'
        return format_html('<a href="{}" target="_blank">{}</a>', url, self.content)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论管理"

    def __str__(self):
        return self.content

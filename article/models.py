from django.db import models
from django.contrib.auth.models import User
# from ckeditor.fields import RichTextField
from ueditor.fields import RichTextField


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, verbose_name='分类名', blank=False, null=False)
    alias = models.CharField(max_length=128, verbose_name='别名', db_index=True)
    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类管理"

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='标题', blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=False, null=True, verbose_name='分类')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='发布者', null=True, editable=False)
    hits = models.IntegerField(verbose_name='点击量', default=0, editable=False)
    # content = RichTextField(verbose_name='内容', null=False, blank=False)
    content = RichTextField(verbose_name='内容', null=False, blank=False,
                            config={'aa': '123', 'bb': '321', 'cc': ['1', '2', '3']})
    subject = models.TextField(verbose_name='简介', editable=False)
    image = models.ImageField(upload_to='static/images/', verbose_name='封面', blank=True, null=True)
    createDate = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    tags = models.CharField(max_length=256, verbose_name='标签', blank=True, null=True)
    top_choices = ((0, '否'),
                   (1, '是'),)
    top = models.IntegerField(choices=top_choices, verbose_name='置顶', default=0, )

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章管理"

    def __str__(self):
        return self.title

from django.test import TestCase
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")

django.setup()

# Create your tests here.
from article.models import Cover
# Cover
#
# class TestCase(TestCase):
#     # 测试函数执行前执行
#     def setUp(self):
#         print("======in setUp")
#
#     # 需要测试的内容
#     def test_add(self):
#         pass
#
#         # 需要测试的内容
#
#     # 测试函数执行后执行
#     def tearDown(self):
#         print("======in tearDown")

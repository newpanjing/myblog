import os, sys, django

from django.test import TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myblog.settings")
django.setup()

from draw import draw
from article.models import Cover, Article
import random
from django.db import models

all = Article.objects.all()

total = Cover.objects.count()

for item in all:
    # if item.image != '':
    #     continue
    c = Cover.objects.all()[random.randint(0, total - 1)]
    url = draw.draw(text=item.title, url=c.image.url, font_size=c.font_size, color=c.color, x=c.x, y=c.y)
    item.image.name = url
    print(url)
    item.save()

# all = Cover.objects.all()
# for index, item in enumerate(all):
#     draw.draw(item, name=index, font_size=item.font_size, color=item.color, x=item.x, y=item.y)
#     print(item, index)

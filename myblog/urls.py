"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView
from . import views
from ueditor import site

# 设置登录页
admin.site.site_title = '管理后台'
admin.site.site_header = '博客管理后台'
urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='static/favicon.ico', permanent=True)),
    path('admin/', admin.site.urls),
    path('', views.home),
    path('article/<id>', views.detail),
    path('category', views.category_all),
    path('category/<alias>', views.category),
    path('category/<alias>/<page>', views.category_page),
    path('page/<alias>', views.page),
    path('ueditor/upload', site.handler),
    path('sitemap.xml', views.sitemap),
    path('error/404', views.page_error),
    path('error/500', views.page_error),
    path('oauth/github', views.oauth_github),
    path('oauth/github/callback', views.oauth_github_callback),
    path('comment/post',views.comments_save)
]

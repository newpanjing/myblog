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
from django.urls import include

# 设置登录页
admin.site.site_title = '管理后台'
admin.site.site_header = '博客管理后台'
urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='static/favicon.ico', permanent=True)),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path(r'article/<id>', views.detail, name='article'),
    path(r'category', views.category_all, name='category'),
    path(r'category/<alias>/', views.category, name='category_alias'),
    path('category/<alias>/<page>/', views.category_page),
    path('page/<alias>/', views.page, name='page'),
    path('sitemap.xml', views.sitemap, name='sitemap'),
    path('error/404', views.page_error),
    path('error/500', views.page_error),
    path('oauth/github/', views.oauth_github, name='github'),
    path('oauth/github/callback/', views.oauth_github_callback, name='github_callback'),

    path('oauth/qq/', views.oauth_qq, name='qq'),
    path('oauth/qq/callback', views.oauth_qq_callback, name='qq_callback'),

    path('oauth/seejoke/', views.oauth_seejoke, name='seejoke'),
    path('oauth/seejoke/callback', views.oauth_seejoke_callback, name='seejoke_callback'),

    path('comment/post', views.comments_save, name='comment_post'),
    path(r'search/', include('haystack.urls')),
    path('project/', views.project, name='project'),
    path('project/<name>/', views.project_detail, name='project_detail'),
    path('logout', views.logout, name='logout'),
    path('no', views.no),
    path('mdeditor/', include('mdeditor.urls')),
    path('simplepro/info/',views.simplepro_info)
]

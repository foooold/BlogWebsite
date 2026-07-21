from django.urls import path
from . import api

urlpatterns = [
    path('hello/', api.hello, name='api-hello'),
    path('articles/', api.article_list, name='api-article-list'),
    path('articles/<str:slug>/', api.article_detail, name='api-article-detail'),
    path('tags/', api.tag_list, name='api-tag-list'),
    path('search/', api.search, name='api-search'),
]

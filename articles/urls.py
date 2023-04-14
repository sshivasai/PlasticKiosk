from django.urls import path
from . import views

urlpatterns = [
    path('', views.articles, name='articles'),
    path('article_details/<str:blog_title>/', views.article_details, name='article_details'),
]

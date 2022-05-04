from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('posts/', views.posts),
    path('posts/<slug:slug>/', views.post_detail, name="post-detail"),
    path('read-later/', views.read_later, name="read-later"),
]
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.home),
    path('user_page/', views.user_page),
    path('user_page1/', views.user_page1),
    path('user.json/', views.user_json),
    path('user.json1/', views.user_json1),
]
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('hello/', MyView.as_view()),
    path('books/', test),
    path('test1/', test1),
    path('publishers/', test2),
    path('authors/', test3),
]
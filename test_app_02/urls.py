from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('hello/', MyView.as_view()),
    path('books/', test),
    path('test1/', test1),
    path('publishers/', test2),
    path('authors/', test3),
    path('add_authors/', add_authors),
    path('add_book/', add_book),
]
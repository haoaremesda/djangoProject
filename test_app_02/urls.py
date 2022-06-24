from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('hello/', MyView.as_view()),
    path('test/', test),
    path('test1/', test1),
]
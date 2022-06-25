import json
import time

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from test_app_02.models import *
from django.core import serializers


class MyView(View):
    def get(self, request):
        # Person.objects.create(name="王五")
        return render(request, 'echarts.html')

def test(request):
    start_time = time.time()
    # books = Book.objects.all()[: 3]
    # for book in books:
    #     print(book.name, book.publisher.name)
    book = Book.objects.filter(name="xRaspberry")
    end_time = time.time()
    print(f"test本次查询花费时长：{end_time-start_time}")
    return JsonResponse({})

def test1(request):
    start_time = time.time()
    authors = Author.objects.all()[: 5]
    # data = serializers.serialize("json", books)
    end_time = time.time()
    print(f"test1本次查询花费时长：{end_time-start_time}")
    # return JsonResponse({"books": json.loads(data)})
    return render(request, "books.html", {"data": authors})

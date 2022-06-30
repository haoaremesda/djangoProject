import json
import time

from django.db.models import Prefetch, Q
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from test_app_02.models import *
from django.core import serializers

from test_app_02.serializers import BookSerializer, PublisherSerializer


class MyView(View):
    def get(self, request):
        # Person.objects.create(name="王五")
        return render(request, 'echarts.html')


def test(request):
    start_time = time.time()
    # books = Book.objects.all()[: 3]
    # for book in books:
    #     print(book.name, book.publisher.name)
    books = Book.objects.filter(Q(name="Abe Akina")).prefetch_related("publisher").prefetch_related(
        "author").prefetch_related("author__city")
    book_data = BookSerializer(books, many=True).data
    # book_data = serializers.serialize("json", books, use_natural_foreign_keys=False)
    # book_data = [model_to_dict(book) for book in books]
    # print(len(books))
    end_time = time.time()
    print(f"test本次查询花费时长：{end_time - start_time}")
    return JsonResponse({"data": book_data})


def test1(request):
    start_time = time.time()
    books = Book.objects.filter(id__gt=5)
    publishers = Publisher.objects.filter(name="Raymond Olson").prefetch_related(
        Prefetch('book_set', queryset=books, to_attr='aidgt5'))
    publisher_data = serializers.serialize("json", publishers)
    end_time = time.time()
    print(f"test1本次查询花费时长：{end_time - start_time}")
    # return JsonResponse({"books": json.loads(data)})
    return JsonResponse({"data": publisher_data})


def test2(request):
    start_time = time.time()
    publishers = Publisher.objects.filter(name="Raymond Olson").prefetch_related(*["book_set", "book_set__author"])
    publisher_data = PublisherSerializer(publishers, many=True).data
    end_time = time.time()
    print(f"test1本次查询花费时长：{end_time - start_time}")
    # return JsonResponse({"books": json.loads(data)})
    return JsonResponse({"data": publisher_data})

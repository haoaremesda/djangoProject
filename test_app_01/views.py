import time

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers
from test_app_01.models import User
from django.db.models import Sum


def home(request):
    user = User.objects.filter(id=1).first()
    # user = User.objects.all()
    # user = serializers.serialize('json', user)
    user = model_to_dict(user)
    return render(request, 'echarts.html', {"datas": [user]})


def user_page(request):
    return render(request, "user_page.html")


def user_page1(request):
    return render(request, "user_page1.html")


def user_json(request):
    from django.core.paginator import Paginator
    from django.core.cache import cache
    contain = {}
    page = int(request.GET.get('page', 1))  # 获取第几页
    limit = int(request.GET.get('limit', 3))  # 每页有多少条数据
    contains = request.GET.get('conditions')
    if contains:
        k = contains.split("=")
        contain[k[0]] = k[1]
        # count = all_count.count()
        print("q")
    all_count = User.objects.filter(**contain).all()
    start_time = time.time()
    # cache_key = f"user_count&{contains}"
    # count = cache.get(cache_key)
    # if not count:
    #     count = User.objects.filter(**contain).count()
    #     cache.set(cache_key, count, nx=False, timeout=1 * 60)
    #     print("user_json写入数据总数")
    # count = User.objects.filter(**contain).count()
    count = all_count.count()
    paginator = Paginator(all_count, limit)
    page_1 = paginator.get_page(page)
    data_list = [model_to_dict(i) for i in page_1]
    end_time = time.time()
    print(f"user_json查询数据总数花费时长：{end_time - start_time} 秒")
    data = {'code': 0, "msg": '操作成功', "data": data_list, 'count': count}
    # data = {'code': 0, "msg": '操作成功', "data": data_list, 'count': paginator.count}
    return JsonResponse(data)


def user_json1(request):
    from django.core.paginator import Paginator
    from django.core.cache import cache
    cache_key = "user_count1"
    page = int(request.GET.get('page', 1))  # 获取第几页
    limit = int(request.GET.get('limit', 3))  # 每页有多少条数据
    start, end = (page - 1) * limit, page * limit
    all_count = User.objects.all()
    start_time = time.time()
    count = cache.get(cache_key)
    if not count:
        count = User.objects.count()
        cache.set(cache_key, count, nx=False, timeout=5 * 60)
        print("user_json1写入数据总数")
    end_time = time.time()
    print(f"user_json1查询数据总数花费时长：{end_time - start_time} 秒")
    paginator = Paginator(all_count, limit)
    page_1 = paginator.get_page(page)
    data_list = [model_to_dict(i) for i in page_1]
    data = {'code': 0, "msg": '操作成功', "data": data_list, 'count': count}
    # data = {'code': 0, "msg": '操作成功', "data": data_list, 'count': paginator.count}
    return JsonResponse(data)


def user_page2(request):
    user = User.objects.all()[0: 10]
    # user = User.objects.all()
    # user = serializers.serialize('json', user)
    return render(request, 'user_page2.html', {"datas": user})
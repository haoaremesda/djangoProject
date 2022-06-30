from rest_framework import routers, serializers
from .models import *


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Author
        fields = '__all__'


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        # fields = '__all__'
        fields = ["id", "name", "book_set"]
        depth = 1


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True)
    publisher = PublisherSerializer()

    class Meta:
        model = Book
        fields = '__all__'
        depth = 1
        # 排除指定的字段
        # exclude = ['id']


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

from rest_framework import routers, serializers
from .models import *


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    # city = CitySerializer()

    class Meta:
        model = Author
        # fields = '__all__'
        fields = ["id", "name", "age", "city", "book_set"]
        depth = 1

    def create(self, validated_data):
        # 处理外键字段
        return Author.objects.create(city=self.context["city"], **validated_data)


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        # fields = '__all__'
        fields = ["id", "name", "book_set"]
        depth = 1


class BookSerializer(serializers.ModelSerializer):
    # author = AuthorSerializer(many=True)
    # publisher = PublisherSerializer()

    class Meta:
        model = Book
        fields = '__all__'
        depth = 1
        # 排除指定的字段
        # exclude = ['id']

    def create(self, validated_data):
        # 处理外键字段与多对多字段
        publisher_id = dict(self.initial_data).get('publisher_idx', [])
        publisher = Publisher.objects.filter(id=publisher_id).first()
        author_id = dict(self.initial_data).get('author_id', [])
        book = Book.objects.create(publisher=publisher, **validated_data)
        for i in author_id:
            book.author.add(i)
        return book


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

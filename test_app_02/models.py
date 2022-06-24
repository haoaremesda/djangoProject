from django.db import models


# 城市
class City(models.Model):
    name = models.CharField(max_length=100)


# 作者
class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)  # 城市


# 出版社
class Publisher(models.Model):
    name = models.CharField(max_length=300)


# 书籍
class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    author = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)


# 商店
class Store(models.Model):
    name = models.CharField(max_length=300)
    book = models.ManyToManyField("Book")

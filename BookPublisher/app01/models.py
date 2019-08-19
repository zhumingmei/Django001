from django.db import models


# Create your models here.
class Publisher(models.Model):
    pid = models.AutoField(primary_key=True)  # id自增 主键
    name = models.CharField(max_length=40, unique=True)  # 不可重复


class Book(models.Model):
    title = models.CharField(max_length=40)
    pub = models.ForeignKey('Publisher', on_delete=models.CASCADE)  # 级联删除

# 通过关系管理对象去拿相应的数据
class Author(models.Model):
    name = models.CharField(max_length=30) # 此举定义了app01_author表，也就是作者这张表
    books = models.ManyToManyField('Book') # 此句定义了app01_author_books这张表，也就是第三张表
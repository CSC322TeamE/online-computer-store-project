from django.db import models

# Create your models here.


class Users(models.Model):
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class Items(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField()
    quantity = models.IntegerField(default=0)
    discount = models.FloatField()
    rating = models.FloatField()
    keyword = models.CharField(max_length=10)
    quantity_sold = models.IntegerField(default=0)





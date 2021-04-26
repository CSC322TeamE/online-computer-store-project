from django.contrib.auth.models import User
from django.db import models


class Customer(User):
    balance = models.FloatField(default=0.0)

    class Meta:
        permissions = [
            ("add_balance", "can add balance"),
        ]


class Clerk(User):
    pass


class Manager(Clerk):
    pass


class Company(User):
    pass


class DeliveryCompany(User):
    pass


class Item(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField()
    quantity = models.IntegerField(default=0)
    discount = models.FloatField()
    rating = models.FloatField()
    keyword = models.CharField(max_length=10)
    quantity_sold = models.IntegerField(default=0)


class CPU(Item):
    category = models.CharField(max_length=10) #
    core_name = models.CharField(max_length=10) # either intel or AMD
    num_cores = models.IntegerField(default=0)
    frequency = models.FloatField(default=0.0)


class GPU(Item):
    category = models.CharField(max_length=10)  # desktop or workstation
    chipset = models.CharField(max_length=10)  # either nvidia or AMD
    num_cuda_cores = models.IntegerField(default=0)
    core_clock = models.FloatField(default=0.0)


class Memory(Item):
    capacity = models.FloatField(default=0.0)


class Computer(Item):
    category = models.CharField(max_length=20)  # business, computing, gaming ...
    os = models.CharField(max_length=10) # operating system
    cpu_id = models.IntegerField()  # cpu
    gpu_id = models.IntegerField()  # gpu
    memory_id = models.IntegerField()  # memory

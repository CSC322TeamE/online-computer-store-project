from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.template.defaultfilters import slugify
import uuid


class Customer(User):
    balance = models.FloatField(default=0.0)
    saved_address = models.CharField(max_length=50, null=True, blank=True, default=None)

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
    brand = models.CharField(max_length=20, null=True, blank=True, default=None)
    price = models.FloatField(null=True, blank=True, default=None)
    quantity = models.IntegerField(null=True, blank=True, default=None)
    discount = models.FloatField(null=True, blank=True, default=None)
    rating = models.FloatField(null=True, blank=True, default=None)
    quantity_sold = models.IntegerField(null=True, blank=True, default=0)
    img = models.ImageField(upload_to='img/item_img/', default='img/default_img/400x650.png', blank=True, null=True)
    url_slug = models.SlugField(editable=False, default="")
    description = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.url_slug = slugify(self.name)
        super(Item, self).save(*args, **kwargs)


class CPU(Item):
    architecture = models.CharField(max_length=10, null=True, blank=True, default=None)  # either intel or AMD
    num_cores = models.IntegerField(null=True, blank=True, default=None)
    frequency = models.FloatField(null=True, blank=True, default=None)


class GPU(Item):
    chipset = models.CharField(max_length=10, null=True, blank=True, default=None)  # either nvidia or AMD
    num_cuda_cores = models.IntegerField(null=True, blank=True, default=0)
    core_clock = models.FloatField(null=True, blank=True, default=0.0)


class Memory(Item):
    capacity = models.FloatField(null=True, blank=True, default=0.0)


class Computer(Item):
    os = models.CharField(max_length=10, null=True, blank=True, default=None)  # operating system
    cpu_name = models.CharField(max_length=20, null=True, blank=True, default=None)
    gpu_name = models.CharField(max_length=20, null=True, blank=True, default=None)
    memory_name = models.CharField(max_length=20, null=True, blank=True, default=None)


class Bank(models.Model):
    pwd = models.CharField(max_length=4)
    customer_name = models.CharField(max_length=20)
    card_number = models.IntegerField(validators=[MaxLengthValidator(6), MinLengthValidator(6)])  # fix length 6


class Transaction(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.FloatField(blank=True)
    time = models.DateTimeField(auto_now_add=True, blank=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uid = models.UUIDField() # a unique uniformed id for each order
    status = models.CharField(max_length=20, default="open")
    address = models.CharField(max_length=50, blank=False, null=False)

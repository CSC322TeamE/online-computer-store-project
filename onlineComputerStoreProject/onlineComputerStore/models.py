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


class CreditCard(models.Model):
    name = models.CharField(max_length=20)
    card_number = models.CharField(max_length=20)
    csc = models.CharField(max_length=3)
    expired_date = models.CharField(max_length=5)


class Forum(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000, blank=True)
    link = models.CharField(max_length=100, blank=True)
    url_slug = models.SlugField(editable=False, default="")

    def __str__(self):
        return str(self.item.name)

    def save(self, *args, **kwargs):
        self.url_slug = slugify(self.item.name)
        super(Forum, self).save(*args, **kwargs)


class Discussion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    discuss = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user.username) + str(self.forum)


class Warning(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, null=True, editable=True)
    description = models.CharField(max_length=300, blank=False)
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE)
    finalized = models.BooleanField(default=False)


class ForumWarning(Warning):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    discuss = models.ForeignKey(Discussion, on_delete=models.CASCADE)


class Transaction(models.Model):
    transaction_number = models.UUIDField(default=uuid.uuid1, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default="")
    amount = models.FloatField(default=0)
    time = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, default=None)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, null=True, default=None)
    order_number = models.UUIDField(editable=False, default=uuid.uuid1()) # a unique uniformed id for each order
    status = models.CharField(max_length=20, default="in progress") # need a clerk to check the order
    address = models.CharField(max_length=50, null=True, default=None)
    delivery_company = models.ForeignKey(DeliveryCompany, on_delete=models.CASCADE, null=True, default=None)



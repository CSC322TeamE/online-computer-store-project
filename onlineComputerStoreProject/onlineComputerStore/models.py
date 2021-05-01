from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.template.defaultfilters import slugify


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
    category = models.CharField(max_length=10)  #
    core_name = models.CharField(max_length=10)  # either intel or AMD
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
    os = models.CharField(max_length=10)  # operating system
    cpu_id = models.IntegerField()  # cpu
    gpu_id = models.IntegerField()  # gpu
    memory_id = models.IntegerField()  # memory


class Bank(models.Model):
    pwd = models.CharField(max_length=4)
    customer_name = models.CharField(max_length=20)
    card_number = models.IntegerField(validators=[MaxLengthValidator(6), MinLengthValidator(6)])  # fix length 6


class Transaction(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.FloatField(blank=True)
    time = models.DateTimeField(auto_now_add=True, blank=True)


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
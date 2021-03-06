from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db.models import Count
from django.template.defaultfilters import slugify
import uuid
from django.core.mail import send_mail
from django.shortcuts import render, redirect


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
    rating = models.FloatField(null=True, blank=True, default=None)


class Item(models.Model):
    name = models.CharField(max_length=20)
    brand = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=False, default=None)
    price = models.FloatField(null=True, blank=False, default=None)
    quantity = models.IntegerField(null=True, blank=False, default=None)
    discount = models.FloatField(null=False, blank=False, default=1)
    rating = models.FloatField(null=True, blank=True, default=None)
    quantity_sold = models.IntegerField(null=True, blank=True, default=0)
    img = models.ImageField(upload_to='img/item_img/', default='img/default_img/400x650.png', blank=True, null=True)
    url_slug = models.SlugField(editable=False, default="")
    description = models.CharField(max_length=50, null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        self.url_slug = slugify(self.name)
        super(Item, self).save(*args, **kwargs)
        forum = Forum(item=self)
        forum.save()  # create forum as item created


class CPU(Item):
    architecture = models.CharField(max_length=10, null=True, blank=True, default=None)  # arm or x86
    num_cores = models.IntegerField(null=True, blank=True, default=None)
    frequency = models.FloatField(null=True, blank=True, default=None)
    power = models.FloatField(null=True, blank=True, default=None)


class GPU(Item):
    chipset = models.CharField(max_length=10, null=True, blank=True, default=None)  # either nvidia or AMD
    num_cuda_cores = models.IntegerField(null=True, blank=True, default=None)
    core_clock = models.FloatField(null=True, blank=True, default=None)
    memory_size = models.FloatField(null=True, blank=True, default=None)
    power = models.FloatField(null=True, blank=True, default=None)


class Memory(Item):
    capacity = models.FloatField(null=True, blank=True, default=0.0)
    type = models.CharField(max_length=5, null=True, blank=True, default=None)  # DDR4 DDR3 ...
    frequency = models.IntegerField(null=True, blank=True, default=None)  #


class HDD(Item):
    capacity = models.FloatField(null=True, blank=True, default=0.0)
    rpm = models.IntegerField(null=True, blank=True)


class Monitor(Item):
    screen_size = models.IntegerField(null=True, blank=True)  # 15 16 17 ...
    resolution = models.CharField(null=True, blank=True, max_length=20)
    refresh_rate = models.IntegerField(null=True, blank=True)


class Battery(Item):
    capacity = models.IntegerField(null=True, blank=True)  # 3000 mAh


class Computer(Item):
    os = models.CharField(max_length=10, null=True, blank=True, default=None)  # operating system
    computer_cpu = models.ForeignKey(CPU, on_delete=models.DO_NOTHING, null=True, blank=False, default=None)
    computer_gpu = models.ForeignKey(GPU, on_delete=models.DO_NOTHING, null=True, blank=False, default=None)
    computer_memory = models.ForeignKey(Memory, on_delete=models.DO_NOTHING, null=True, blank=False, default=None)
    computer_hdd = models.ForeignKey(HDD, on_delete=models.DO_NOTHING, null=True, blank=False, default=None)
    computer_monitor = models.ForeignKey(Monitor, on_delete=models.DO_NOTHING, null=True, blank=False, default=None)
    computer_battery = models.ForeignKey(Battery, on_delete=models.DO_NOTHING, null=True, blank=True, default=None)


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
    url_slug = models.SlugField(editable=False, default="")

    def __str__(self):
        return str(self.item.name)

    def save(self, *args, **kwargs):
        if not Forum.objects.filter(item_id=self.item.id).exists():
            self.url_slug = slugify(self.item.name)
            super(Forum, self).save(*args, **kwargs)


class Discussion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    discuss = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    reply_to = models.IntegerField(editable=False, null=True)

    def __str__(self):
        return str(self.user.username) + str(self.forum)


class Warning(models.Model):  # forum auto created ID are saved here since no reporter.
    date_created = models.DateTimeField(auto_now_add=True, null=True, editable=True)
    description = models.CharField(max_length=300, blank=False)
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE)
    finalized = models.BooleanField(default=False)
    justification = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super(Warning, self).save(*args, **kwargs)
        finalized_warning_count = Warning.objects.filter(reported_user=self.reported_user, finalized=True).count()
        if finalized_warning_count >= 3 and not SuspendedList.objects.filter(user=self.reported_user).exists():
            SuspendedList.objects.create(user=self.reported_user, email=self.reported_user.email)
            message = "New suspended user added to list!"


class ForumWarning(Warning):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    discuss = models.ForeignKey(Discussion, on_delete=models.CASCADE)


class OrderWarning(Warning):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)


class Transaction(models.Model):
    transaction_number = models.UUIDField(default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default="")
    amount = models.FloatField(default=0)
    time = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, default=None)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, default=None)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, null=True, default=None)
    order_number = models.UUIDField(editable=False, default=uuid.uuid4)  # a unique uniformed id for each order
    status = models.CharField(max_length=20, default="in progress")  # need a clerk to check the order
    address = models.CharField(max_length=50, null=True, default=None)
    delivery_company = models.ForeignKey(DeliveryCompany, on_delete=models.CASCADE, null=True, default=None)
    assigned_by = models.ForeignKey(Clerk, on_delete=models.SET_NULL, null=True)
    justification = models.CharField(max_length=1000, blank=True)
    url_slug = models.SlugField(editable=False, default="")
    item_score = models.FloatField(null=True, blank=True, default=None)
    delivery_score = models.FloatField(null=True, blank=True, default=None)
    tracking_info = models.CharField(max_length=50, null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        self.url_slug = slugify(self.order_number)
        super(Order, self).save(*args, **kwargs)


class Bidfor(models.Model):
    price = models.FloatField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery_company = models.ForeignKey(DeliveryCompany, on_delete=models.CASCADE)

    class Meta:
        ordering = ['delivery_company', 'order']


class TabooList(models.Model):
    addBy = models.ForeignKey(Clerk, on_delete=models.CASCADE)
    word = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.word = self.word.upper()
        super(TabooList, self).save(*args, **kwargs)


class SuspendedList(models.Model):

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    justification = models.TextField(blank=True)
    email = models.CharField(blank=True, max_length=100)

    def save(self, *args, **kwargs):
        send_mail(
            'Online Computer Store Alert',
            'Your account is suspended since 3 standing warnings in your account(or by the decision of the manager)! This is your last chance(in a week) to clean up your account.',
            'onlineComputerStoreGroup@gmail.com',
            [self.email],
            fail_silently=False,
        )
        super(SuspendedList, self).save(*args, **kwargs)


class SuggestedItem(models.Model):
    item1 = models.ForeignKey(Item, related_name='suggested_item1', on_delete=models.CASCADE, null=True, blank=True, default=None)
    item2 = models.ForeignKey(Item, related_name='suggested_item2', on_delete=models.CASCADE, null=True, blank=True,
                              default=None)
    item3 = models.ForeignKey(Item, related_name='suggested_item3', on_delete=models.CASCADE, null=True, blank=True,
                              default=None)



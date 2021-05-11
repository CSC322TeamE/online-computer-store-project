from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import Group, Permission
from onlineComputerStore.models import *


def add_user():
    if not Group.objects.filter(name="clerks"):
        group = Group.objects.create(name='clerks')
        can_add_item = Permission.objects.get(codename='add_item')
        group.permissions.add(can_add_item)

    if not Group.objects.filter(name="customers"):
        group = Group.objects.create(name='customers')
        can_add_balance = Permission.objects.get(codename='add_balance')
        group.permissions.add(can_add_balance)

    if not Group.objects.filter(name="managers"):
        group = Group.objects.create(name='managers')
        can_add_item = Permission.objects.get(codename='add_item')
        group.permissions.add(can_add_item)

    if not Group.objects.filter(name="companies"):
        group = Group.objects.create(name='companies')

    if not Group.objects.filter(name="deliverycompanies"):
        group = Group.objects.create(name='deliverycompanies')

    if not Customer.objects.filter(username="customer").exists():
        user = Customer.objects.create_user(username="customer", password="customer")
        group = Group.objects.get(name='customers')
        user.groups.add(group)

    if not Clerk.objects.filter(username="clerk").exists():
        user = Clerk.objects.create_user(username="clerk", password="clerk")
        group = Group.objects.get(name='clerks')
        user.groups.add(group)

    if not Manager.objects.filter(username="manager").exists():
        user = Manager.objects.create_user(username="manager", password="manager")
        group = Group.objects.get(name='managers')
        user.groups.add(group)


#Dlivery Company
    if not DeliveryCompany.objects.filter(username="UPS").exists():
        user = DeliveryCompany.objects.create_user(username="UPS", password="UPS")
        group = Group.objects.get(name='deliverycompanies')
        user.groups.add(group)

    if not DeliveryCompany.objects.filter(username="FEDEX").exists():
        user = DeliveryCompany.objects.create_user(username="FEDEX", password="FEDEX")
        group = Group.objects.get(name='deliverycompanies')
        user.groups.add(group)



    if not Company.objects.filter(username="INTEL").exists():
        user = Company.objects.create_user(username="INTEL", password="INTEL")
        group = Group.objects.get(name='companies')
        user.groups.add(group)

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

    if not Clerk.objects.filter(username="ShuoXin Liu").exists():
        user = Clerk.objects.create_user(username="ShuoXin Liu", password="ShuoXin Liu")
        group = Group.objects.get(name='clerks')
        user.groups.add(group)

    if not Clerk.objects.filter(username="Yi Lin").exists():
        user = Clerk.objects.create_user(username="Yi Lin", password="Yi Lin")
        group = Group.objects.get(name='clerks')
        user.groups.add(group)

    if not Clerk.objects.filter(username="Ling Fang").exists():
        user = Clerk.objects.create_user(username="Ling Fang", password="Ling Fang")
        group = Group.objects.get(name='clerks')
        user.groups.add(group)

    if not Clerk.objects.filter(username="Yi Yang Wu").exists():
        user = Clerk.objects.create_user(username="Yi Yang Wu", password="Yi Yang Wu")
        group = Group.objects.get(name='clerks')
        user.groups.add(group)

    if not Clerk.objects.filter(username="Alice Chen").exists():
        user = Clerk.objects.create_user(username="Alice Chen", password="Alice Chen")
        group = Group.objects.get(name='clerks')
        user.groups.add(group)

    if not Manager.objects.filter(username="manager").exists():
        user = Manager.objects.create_user(username="manager", password="manager")
        group = Group.objects.get(name='managers')
        user.groups.add(group)

    # Dlivery Company
    if not DeliveryCompany.objects.filter(username="UPS").exists():
        user = DeliveryCompany.objects.create_user(username="UPS", password="UPS")
        group = Group.objects.get(name='deliverycompanies')
        user.groups.add(group)

    if not DeliveryCompany.objects.filter(username="FEDEX").exists():
        user = DeliveryCompany.objects.create_user(username="FEDEX", password="FEDEX")
        group = Group.objects.get(name='deliverycompanies')
        user.groups.add(group)

    if not DeliveryCompany.objects.filter(username="DHL").exists():
        user = DeliveryCompany.objects.create_user(username="DHL", password="DHL")
        group = Group.objects.get(name='deliverycompanies')
        user.groups.add(group)

    if not DeliveryCompany.objects.filter(username="USPS").exists():
        user = DeliveryCompany.objects.create_user(username="USPS", password="USPS")
        group = Group.objects.get(name='deliverycompanies')
        user.groups.add(group)

    if not DeliveryCompany.objects.filter(username="Purolator").exists():
        user = DeliveryCompany.objects.create_user(username="Purolator", password="Purolator")
        group = Group.objects.get(name='deliverycompanies')
        user.groups.add(group)

    if not DeliveryCompany.objects.filter(username="OnTrac Inc.").exists():
        user = DeliveryCompany.objects.create_user(username="OnTrac Inc.", password="OnTrac Inc.")
        group = Group.objects.get(name='deliverycompanies')
        user.groups.add(group)
    if not Company.objects.filter(username="INTEL").exists():
        user = Company.objects.create_user(username="INTEL", password="INTEL")
        group = Group.objects.get(name='companies')
        user.groups.add(group)

    if not Company.objects.filter(username="AMD").exists():
        user = Company.objects.create_user(username="AMD", password="AMD")
        group = Group.objects.get(name='companies')
        user.groups.add(group)

    if not Company.objects.filter(username="HP").exists():
        user = Company.objects.create_user(username="HP", password="HP")
        group = Group.objects.get(name='companies')
        user.groups.add(group)

    if not Company.objects.filter(username="APPLE").exists():
        user = Company.objects.create_user(username="APPLE", password="APPLE")
        group = Group.objects.get(name='companies')
        user.groups.add(group)

    if not Company.objects.filter(username="DELL").exists():
        user = Company.objects.create_user(username="DELL", password="DELL")
        group = Group.objects.get(name='companies')
        user.groups.add(group)

    if not Company.objects.filter(username="LENOVO").exists():
        user = Company.objects.create_user(username="LENOVO", password="LENOVO")
        group = Group.objects.get(name='companies')
        user.groups.add(group)

    if not Company.objects.filter(username="ACER").exists():
        user = Company.objects.create_user(username="ACER", password="ACER")
        group = Group.objects.get(name='companies')
        user.groups.add(group)

    if not Company.objects.filter(username="MICROSOFT").exists():
        user = Company.objects.create_user(username="MICROSOFT", password="MICROSOFT")
        group = Group.objects.get(name='companies')
        user.groups.add(group)

    if not Company.objects.filter(username="SAMSUNG").exists():
        user = Company.objects.create_user(username="SAMSUNG", password="SAMSUNG")
        group = Group.objects.get(name='companies')
        user.groups.add(group)
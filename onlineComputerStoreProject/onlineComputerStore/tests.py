from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import Group
from onlineComputerStore.models import Clerk,Manager


def add_user():
    if not Manager.objects.filter(username="manager01").exists():
        user = Manager.objects.create_user(username="manager01", password="manager01")
        user.save()
        group = Group.objects.get(name='managers')
        user.groups.add(group)
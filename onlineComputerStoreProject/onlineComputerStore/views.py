from django.shortcuts import render, redirect
from onlineComputerStore.models import Users
from django.contrib import messages
from onlineComputerStore.models import Items


# Create your views here.


def index(request):
    suggested_list = ['s1', 's2', 's3']
    popular_list = Items.objects.order_by('quantity_sold')[0:3]
    return render(request, 'index.html', {'popular_list': popular_list, 'suggested_list': suggested_list})


def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        if Users.objects.all().filter(username=username).filter(password=password).exists():
            return redirect('/regUser/', {'user': username})

    return render(request, 'login.html')


def register(request):
    if 'email' in request.POST and 'username' in request.POST and 'password' in request.POST:
        if Users.objects.all().filter(username=request.POST['username']).exists():
            messages.info(request, 'Please use another username')
            return render(request, 'register.html')

        if Users.objects.all().filter(email=request.POST['email']).exists():
            messages.info(request, 'Please use another email')
            return render(request, 'register.html')

        Users.objects.create(username=request.POST['username'],
                             email=request.POST['email'],
                             password=request.POST['password'])

        return redirect('/login/')

    return render(request, 'register.html')


def clerk(request):
    return render(request, 'clerk.html')


def manager(request):
    return render(request, 'manager.html')


def regUser(request):
    return render(request, 'regUser.html')






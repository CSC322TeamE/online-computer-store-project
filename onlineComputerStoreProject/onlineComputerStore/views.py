from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render_to_response

# Create your views here.


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    if request.POST:
        return render(request, 'register.html', context={'success': 'true'},)
    return render(request, 'register.html')



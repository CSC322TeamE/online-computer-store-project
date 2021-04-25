from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, redirect
from onlineComputerStore.models import Customer, Clerk, Manager, CPU, GPU, Memory, Computer
from django.contrib import messages, auth
from onlineComputerStore.models import Item
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required, login_required
import onlineComputerStore.tests as ts


def index(request):
    ts.add_user()
    if request.user.is_authenticated:
        return render(request, 'userIndex.html')

    else:
        suggested_list = ['s1', 's2', 's3']
        popular_list = Item.objects.order_by('quantity_sold')[0:3]
        return render(request, 'index.html', {'popular_list': popular_list, 'suggested_list': suggested_list})


def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('/', {'user': user})

        messages.info(request, 'username and password does not match')

    return render(request, 'login.html')


def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    else:
        if 'email' in request.POST and 'username' in request.POST and 'password' in request.POST:
            if Customer.objects.filter(username=request.POST['username']).exists():
                messages.info(request, 'another username')
                return render(request, 'register.html')

            if Customer.objects.filter(email=request.POST['email']).exists():
                messages.info(request, 'another email')
                return render(request, 'register.html')

            user = Customer.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            user.save()
            group = Group.objects.get(name='customers')
            user.groups.add(group)
            return redirect('/login/')


def logout(request):
    auth.logout(request)
    return redirect('/login')


@login_required
def account(request):
    # if the user is a customer:
    if request.user.groups.filter(name='customers').exists():
        return render(request, 'customer.html')

    if request.user.groups.filter(name='clerks').exists():
        return render(request, 'clerk.html')

    if request.user.groups.filter(name='managers').exists():
        return render(request, 'manager.html')


@permission_required('onlineComputerStore.add_item', login_url="/login/")
def addItem(request):
    if request.method == "POST" and 'name' in request.POST:
        '''item = Item.objects.create(
            name=request.POST['name'],
            price=request.POST['price'],
            quantity=request.POST['quantity'],
            discount=request.POST['discount'],
            rating=request.POST['rating'],
            keyword=request.POST['keyword'],
            quantity_sold=request.POST['quantity_sold']
        )
        item.save()'''

        if request.POST['type'] == 'cpu':
            obj = CPU.objects.create(
                name=request.POST['name'],
                price=request.POST['price'],
                quantity=request.POST['quantity'],
                discount=request.POST['discount'],
                rating=request.POST['rating'],
                keyword=request.POST['keyword'],
                quantity_sold=request.POST['quantity_sold'],
                category=request.POST['category'],
                core_name=request.POST['core_name'],
                num_cores=request.POST['num_cores'],
                frequency=request.POST['frequency']
            )
            obj.save()
            str += 'cpu'

        if request.POST['type'] == 'gpu':
            obj = GPU.objects.create(
                name=request.POST['name'],
                price=request.POST['price'],
                quantity=request.POST['quantity'],
                discount=request.POST['discount'],
                rating=request.POST['rating'],
                keyword=request.POST['keyword'],
                quantity_sold=request.POST['quantity_sold'],
                category=request.POST['category'],
                chipset=request.POST['chipset'],
                num_cuda_cores=request.POST['num_cuda_cores'],
                core_clock=request.POST['core_clock']
            )
            obj.save()
            str += "gpu"

        if request.POST['type'] == 'memory':
            obj = Memory.objects.create(
                name=request.POST['name'],
                price=request.POST['price'],
                quantity=request.POST['quantity'],
                discount=request.POST['discount'],
                rating=request.POST['rating'],
                keyword=request.POST['keyword'],
                quantity_sold=request.POST['quantity_sold'],
                capacity=request.POST['capacity'],
            )
            obj.save()
            str += "memory"

        if request.POST['type'] == 'computer':
            obj = Computer.objects.create(
                name=request.POST['name'],
                price=request.POST['price'],
                quantity=request.POST['quantity'],
                discount=request.POST['discount'],
                rating=request.POST['rating'],
                keyword=request.POST['keyword'],
                quantity_sold=request.POST['quantity_sold'],
                category=request.POST['category'],
                os=request.POST['os'],
                cpu_id=request.POST['cpuid'],
                gpu_id=request.POST['gpuid'],
                memory_id=request.POST['memid']
            )
            obj.save()
            str += "computer"

        messages.info(request, str)
        return render(request, 'addItem.html')

    else:
        return render(request, 'addItem.html')


def browse(request):
    return render(request, 'browse.html')




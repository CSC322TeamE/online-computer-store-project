from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required, login_required
import onlineComputerStore.tests as ts
from .forms import *


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


def topUp(request):
    if request.method == "POST":
        if Bank.objects.filter(card_number=request.POST['card_num']).exists():
            obj = Bank.objects.get(card_number=request.POST['card_num'])
            if request.POST['customer_name'] == obj.customer_name and request.POST['pwd'] == obj.pwd:
                customer = Customer.objects.get(id=request.user.id)
                customer.balance += float(request.POST['amount'])
                customer.save()
                tran = Transaction.objects.create(customer_id=customer, amount=request.POST['amount'])
                tran.save()
                messages.info(request, "Success!!!")
            else:
                messages.error(request, "Information doesnt match!!!")
        else:
            messages.info(request, "This bank customer does not exist!!!")
    return render(request, 'topUp.html')


def forum(request):
    forums = Forum.objects.all()
    count = forums.count()
    discussions = []

    for f in forums:
        discussions.append(f.discussion_set.all())

    context = {'forums': forums,
               'count': count,
               'discussions': discussions}
    return render(request, 'forum.html', context)


def addDiscussion(request):
    form = DiscusstionForm()  # not POST
    if request.method == 'POST':

        form = DiscusstionForm(request.POST)
        if form.is_valid():
            forum_instance = form.save(commit=False)
            forum_instance.user_id = request.user.id
            forum_instance.forum_id = request.POST['forum_id']
            forum_instance.save()
            messages.info(request, "Your comments are submitted!")
            return redirect('/forum/')

    context = {'form': form, 'forum_id': request.POST['forum_id']}
    return render(request, 'addDiscussion.html', context)


def forum_report(request):
    form = FroumReportForm()  # not POST
    print(request.POST)
    if request.method == 'POST':
        if 'description' in request.POST:
            form = FroumReportForm(request.POST, initial={'reported_user': request.POST["reportedID"],
                                                          'reporter': request.user.id,
                                                          'discuss': request.POST["discussionID"]})
            print(form)
            if form.is_valid():
                form.save()
                messages.info(request, "Your report is submitted!")
            return redirect('/forum/')

    context = {'form': form, 'discussionID': request.POST["discussionID"], 'reportedID': request.POST['reportedID']}
    return render(request, 'forumReport.html', context)

from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required, login_required
import onlineComputerStore.tests as ts
from .forms import *
# import onlineComputerStore.tests as ts
from onlineComputerStore.forms import AddCpuForm


def index(request):
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

            user = Customer.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
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
    form = AddCpuForm(request.POST, request.FILES)
    if request.method == "POST" and 'name' in request.POST:
        if form.is_valid():
            cd = form.cleaned_data
            if not CPU.objects.filter(name=cd['name']).exists():
                form.save()
            return render(request, 'addItem.html', {'form': form})

        else:
            return render(request, 'addItem.html', {'form': form})

    else:
        return render(request, 'addItem.html', {'form': form})


def browse(request):
    item_list = Item.objects.order_by("quantity_sold")
    return render(request, 'browse.html', {'item_list': item_list})


def topUp(request):
    if request.method == "POST":
        if Bank.objects.filter(card_number=request.POST['card_num']).exists():
            obj = Bank.objects.get(card_number=request.POST['card_num'])
            if request.POST['customer_name'] == obj.customer_name and request.POST['pwd'] == obj.pwd:
                customer = Customer.objects.get(id=request.user.id)
                customer.balance += float(request.POST['amount'])
                customer.save()
                tran = Transaction.objects.create(customer=customer, amount=request.POST['amount'])
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
            form = FroumReportForm(request.POST)
            if form.is_valid():
                forum_warning = form.save(commit=False)
                forum_warning.reporter_id = request.user.id
                forum_warning.reported_user_id = request.POST['reportedID']
                forum_warning.discuss_id = request.POST['discussionID']
                form.save()
                messages.info(request, "Your report is submitted!")
            return redirect('/forum/')

    context = {'form': form, 'discussionID': request.POST["discussionID"], 'reportedID': request.POST['reportedID']}
    return render(request, 'forumReport.html', context)


def item(request, url_slug):
    item = Item.objects.get(url_slug=url_slug)
    return render(request, 'item.html', {'item': item})


def purchase(request, url_slug):
    item = Item.objects.get(url_slug=url_slug)
    customer = Customer.objects.get(id=request.user.id)
    if customer.saved_address == "NULL":
        return render(request, "purchase.html", {'item': item, 'balance': customer.balance})
    else:
        return render(request, "purchase.html", {'item': item, 'balance': customer.balance, 'saved_address': customer.saved_address})


def purchaseConfirm(request, url_slug):
    item = Item.objects.get(url_slug=url_slug)
    if request.method == "POST":

        # confirmation of purchase
        if 'confirm' in request.POST:
            customer = Customer.objects.get(id=request.user.id)
            if request.POST['payment_method'] == "credit card":
                # charge credit card
                pass
            else:
                # charge from user balance
                customer.balance -= item.price
                customer.save()

            # record transaction
            form = TransactionForm(request.POST)
            transaction = form.save(commit=False)
            transaction.customer = customer
            form.save()

            # record order
            form = OrderForm(request.POST)
            order = form.save(commit=False)
            order.customer = customer
            order.transaction = Transaction.objects.filter(customer=customer).latest('id')
            form.save()

            messages.info(request, "purchased successfully")
            return redirect("/")

        # check input credit card is valid
        if request.POST['payment_method'] == 'credit card':
            form = CreditCardForm(request.POST)
            if form.is_valid():
                return render(request, "purchaseConfirm.html", {'item': item,
                                                                'payment_method': request.POST['payment_method'],
                                                                'address': request.POST['address']})
            else:
                error_string = ''.join([''.join(x for x in l) for l in list(form.errors.values())])
                messages.info(request, error_string)
                return redirect("/purchase/"+url_slug)

        # check input balance is enough
        if request.POST['payment_method'] == 'balance':
            if item.price > Customer.objects.get(id=request.user.id).balance:
                messages.info(request, "not enough balance, please topup first")
                return redirect("/purchase/"+url_slug)

            else:
                return render(request, "purchaseConfirm.html", {'item': item,
                                                                'payment_method': request.POST['payment_method'],
                                                                'address': request.POST['address']})

    else:
        return render(request, "purchaseConfirm.html")


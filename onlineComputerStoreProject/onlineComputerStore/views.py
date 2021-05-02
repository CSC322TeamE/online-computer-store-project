from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required, login_required
import onlineComputerStore.tests as ts
from .forms import *
import re
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

            user = Customer.objects.create_user(username=request.POST['username'], password=request.POST['password'])
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
                Transaction.objects.create(customer_id=customer, amount=request.POST['amount'])
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
    if request.method == 'POST':
        if "discuss" in request.POST:
            message = request.POST['discuss']
            for bad_word in TabooList.objects.values('word'):
                message = message.replace(bad_word['word'], len(bad_word['word']) * '*')

            obj = Discussion.objects.create(user_id=request.user.id, forum_id=request.POST['forum_id'],
                                            discuss=message)

            if message == request.POST['discuss']:
                messages.info(request, "Your comments are submitted!")
            else:
                messages.info(request, "Your comments are submitted!")
                Warning.objects.create(reported_user=request.user, description='__Taboo_List_Auto__')
                messages.info(request, "A warning created since your message contains sensitive word(s)!")
            return redirect('/forum/')
        context = {'forum_id': request.POST['forum_id']}
        return render(request, 'addDiscussion.html', context)
    else:
        return render(request, 'addDiscussion.html')


def forum_report(request):
    form = ForumReportForm()  # not POST
    if request.method == 'POST':
        if 'description' in request.POST:
            form = ForumReportForm(request.POST)
            if form.is_valid():
                forum_warning = form.save(commit=False)
                forum_warning.reporter_id = request.user.id
                forum_warning.reported_user_id = request.POST['reportedID']
                forum_warning.discuss_id = request.POST['discussionID']
                form.save()
                messages.info(request, "Your report is submitted!")
                return redirect('/forum/')
            else:
                messages.info(request, "Your input is not valid")
        discussion = Discussion.objects.get(id=request.POST["discussionID"])
        context = {'form': form, 'discussion': discussion, 'discussionID': request.POST["discussionID"],
                   'reportedID': request.POST['reportedID']}
    else:
        context = {'form': form}
    return render(request, 'forumReport.html', context)


def item(request, url_slug):
    item = Item.objects.get(url_slug=url_slug)
    return render(request, 'item.html', {'item': item})


def purchase(request):
    return render(request, 'purchase.html')


def tabooList(request):
    wordlist = list(TabooList.objects.values_list('word', flat=True))
    wordlist = [x.upper() for x in wordlist]
    wordset = set(wordlist)
    if request.method == "POST":
        if "word" in request.POST:
            if ' ' in request.POST['word']:
                messages.info(request, "Warning: Space is not allowed!!!")
            else:
                if TabooList.objects.filter(word=request.POST['word']).exists():
                    messages.info(request, "This word is already in the list.")
                else:
                    for w in TabooList.permute(request.POST['word']):
                        TabooList.objects.create(word=w, addBy_id=request.user.id)

                    txt = "The word {word} has been added successfully."
                    messages.info(request, txt.format(word=request.POST['word']))
    context = {'taboolist': wordset}
    return render(request, 'tabooList.html', context)

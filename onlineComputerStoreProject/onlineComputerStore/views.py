import re
from django.contrib.auth.models import Group, Permission
from django.http import HttpResponse
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required, login_required
import onlineComputerStore.tests as ts
from .forms import *
from django.core.mail import send_mail
from onlineComputerStore.forms import AddCpuForm
from django.db.models import Q, Avg, Count
import datetime
import urllib


def index(request):
    ts.add_user()

    if request.user.is_authenticated:
        if SuggestedItem.objects.all().exists():
            suggested = SuggestedItem.objects.order_by('-id')[0]
            suggested_list = []
            if Item.objects.filter(id=suggested.item1_id).exists():
                suggested_list.append(Item.objects.get(id=suggested.item1_id))

            if Item.objects.filter(id=suggested.item2_id).exists():
                suggested_list.append(Item.objects.get(id=suggested.item2_id))

            if Item.objects.filter(id=suggested.item3_id).exists():
                suggested_list.append(Item.objects.get(id=suggested.item3_id))

        else:
            suggested_list = []
        popular_list = Item.objects.order_by('quantity_sold')[0:3]
        return render(request, 'userIndex.html', {'popular_list': popular_list, 'suggested_list': suggested_list})

    else:
        if SuggestedItem.objects.all().exists():
            suggested = SuggestedItem.objects.order_by('-id')[0]
            suggested_list = []
            if Item.objects.filter(id=suggested.item1_id).exists():
                suggested_list.append(Item.objects.get(id=suggested.item1_id))

            if Item.objects.filter(id=suggested.item2_id).exists():
                suggested_list.append(Item.objects.get(id=suggested.item2_id))

            if Item.objects.filter(id=suggested.item3_id).exists():
                suggested_list.append(Item.objects.get(id=suggested.item3_id))

        else:
            suggested_list = []
        popular_list = Item.objects.order_by('quantity_sold')[0:3]
        return render(request, 'index.html', {'popular_list': popular_list, 'suggested_list': suggested_list})


def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            if SuspendedList.objects.filter(user=user).exists():
                suspended_user = SuspendedList.objects.get(user=user)
                now = datetime.datetime.now().date()
                delta = now - suspended_user.date_created.date()
                if delta.days >= 0:
                    User.objects.get(username=user).delete()
                    messages.info(request, "You account has been suspended!!!")
                    return render(request, 'login.html')
            auth.login(request, user)
            return redirect('/', {'user': user})

        messages.info(request, 'username and password does not match')

    return render(request, 'login.html')


def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    else:
        if 'email' in request.POST and 'username' in request.POST and 'password' in request.POST:
            if User.objects.filter(username=request.POST['username']).exists():
                messages.info(request, 'Please use another username')
                return render(request, 'register.html')

            if User.objects.filter(email=request.POST['email']).exists():
                send_mail(
                    'Online Computer Store Alert',
                    'You already have a account, if you do not know what I am talking about, you should check what happended.',
                    'onlineComputerStoreGroup@gmail.com',
                    [request.POST['email']],
                    fail_silently=False,
                )
                messages.info(request, 'Please use another email.')
                return render(request, 'register.html')

            if SuspendedList.objects.filter(email=request.POST['email']).exists():
                send_mail(
                    'Online Computer Store Alert',
                    'Sorry, this email is in the suspended list, try another one.',
                    'onlineComputerStoreGroup@gmail.com',
                    [request.POST['email']],
                    fail_silently=False,
                )
                messages.info(request, 'Please use another email.')
                return render(request, 'register.html')

            user = Customer.objects.create_user(username=request.POST['username'], email=request.POST['email'],
                                                password=request.POST['password'])
            user.save()
            group = Group.objects.get(name='customers')
            user.groups.add(group)
            messages.info(request, "You are successfully registered!")
            return redirect('/login/')


def logout(request):
    auth.logout(request)
    return redirect('/login')


@login_required
def account(request):
    # if the user is a customer:
    if request.user.groups.filter(name='customers').exists():
        customer = Customer.objects.get(id=request.user.id)
        return render(request, 'customer.html', {'customer': customer})

    if request.user.groups.filter(name='clerks').exists():
        return render(request, 'clerk.html')

    if request.user.groups.filter(name='managers').exists():
        return render(request, 'manager.html')

    if request.user.groups.filter(name='deliverycompanies').exists():
        open_order = Order.objects.filter(status='in progress')
        bided_orderID = Bidfor.objects.filter(delivery_company_id=request.user.id).values_list("order_id", flat=True)
        for order in bided_orderID:
            open_order = open_order.exclude(id=order)
        return render(request, 'delivery.html', context={'open_order': open_order})

    if request.user.groups.filter(name='companies').exists():
        return render(request, 'company.html')

    return HttpResponse("Unknown user groups")


@permission_required('onlineComputerStore.add_item', login_url="/login/")
def addItem(request):
    if request.method == 'POST':
        # if the posted form are cpu form
        if 'is_cpu' in request.POST:
            form = AddCpuForm(request.POST, request.FILES)
            model = CPU

        if 'is_gpu' in request.POST:
            form = AddGpuForm(request.POST, request.FILES)
            model = GPU

        if 'is_memory' in request.POST:
            form = AddMemoryForm(request.POST, request.FILES)
            model = Memory

        if 'is_hdd' in request.POST:
            form = AddHddForm(request.POST, request.FILES)
            model = HDD

        if 'is_monitor' in request.POST:
            form = AddMonitorForm(request.POST, request.FILES)
            model = Monitor

        if 'is_battery' in request.POST:
            form = AddBatteryForm(request.POST, request.FILES)
            model = Battery

        if 'is_computer' in request.POST:
            form = AddComputerForm(request.POST, request.FILES)
            model = Computer

        if form.is_valid():
            cd = form.cleaned_data
            if not model.objects.filter(name=cd['name']).exists():
                form.save()
            messages.info(request, "add item successful")
        else:
            messages.info(request, "something wrong")
        return redirect('/addItem/')

    else:
        cpu_form = AddCpuForm()
        gpu_form = AddGpuForm()
        memory_form = AddMemoryForm()
        hdd_form = AddHddForm()
        monitor_form = AddMonitorForm()
        battery_form = AddBatteryForm()
        computer_form = AddComputerForm()
        return render(request, 'addItem.html', {'cpu_form': cpu_form,
                                                'gpu_form': gpu_form,
                                                'memory_form': memory_form,
                                                'hdd_form': hdd_form,
                                                'monitor_form': monitor_form,
                                                'battery_form': battery_form,
                                                'computer_form': computer_form, })


def browse(request, url_slug=None):
    item_list = Item.objects.all()
    if request.method == "POST":
        if url_slug == "computer":
            form = FilterComputerForm(request.POST)
            item_list = form.get_items()
            return render(request, 'browseComputer.html', {'item_list': item_list,
                                                           'form': form})

        if url_slug == "component":
            if request.POST['component'] == 'cpu':
                item_list = CPU.objects.all()

            if request.POST['component'] == 'gpu':
                item_list = GPU.objects.all()

            if request.POST['component'] == 'memory':
                item_list = Memory.objects.all()

            if request.POST['component'] == 'hdd':
                item_list = HDD.objects.all()

            if request.POST['component'] == 'monitor':
                item_list = Monitor.objects.all()

            if request.POST['component'] == 'battery':
                item_list = Battery.objects.all()

            return render(request, 'browseComponent.html', {'item_list': item_list,
                                                            'component': request.POST['component']})

        if 'search' in request.POST:
            item_list = Item.objects.filter(Q(name__icontains=request.POST['search']) | Q(description__icontains=request.POST['search']))
            return render(request, 'browse.html', {'item_list': item_list})

    else:
        return render(request, 'browse.html', {'item_list': item_list})


def topUp(request):
    if request.method == "POST":
        if Bank.objects.filter(card_number=request.POST['card_num']).exists():
            obj = Bank.objects.get(card_number=request.POST['card_num'])
            if request.POST['customer_name'] == obj.customer_name and request.POST['pwd'] == obj.pwd:
                customer = Customer.objects.get(id=request.user.id)
                customer.balance += float(request.POST['amount'])
                customer.save()
                Transaction.objects.create(customer_id=customer.id, amount=request.POST['amount'])
                text = "Success!!! {amount} dollars have been added to your balance.".format(
                    amount=float(request.POST['amount']))
                messages.info(request, text)
                return redirect('/topUp/')

            else:
                messages.error(request, "Information doesnt match!!!")
        else:
            messages.info(request, "This bank customer does not exist!!!")
    return render(request, 'topUp.html')


def complaint(request):
    if request.method == 'POST':
        if "complainDeliveryCompany" in request.POST:
            OrderWarning.objects.create(reporter=request.user, reported_user_id=request.POST['deliveryCompID'],
                                        description=request.POST['complainDeliveryCompany'])
            messages.info(request, "Your complaint is filed successfully, we will solve it as soon as possible!")
            return redirect("/viewOrder/")
        if "complainComputerCompany" in request.POST:
            OrderWarning.objects.create(reporter=request.user, reported_user_id=request.POST['CompID'],
                                        description=request.POST['complainComputerCompany'])
            messages.info(request, "Your complaint is filed successfully, we will solve it as soon as possible!")
            return redirect("/viewOrder/")
        if "computer_companyID" in request.POST:
            delivery_comp = request.POST["deliveryID"]
            context = {"companyID": request.POST['computer_companyID'], "deliveryID": delivery_comp,
                       "order_number": request.POST['order_number']}
            return render(request, 'complaint.html', context)
        messages.info(request, 'Complaint has been submitted successfully!')
    return render(request, 'complaint.html')


def forum(request):
    forums = Forum.objects.all()
    count = forums.count()
    discussions = []
    for f in forums:
        discussions.append(f.discussion_set.all().filter(reply_to=None))
        replies = Discussion.objects.filter(~Q(reply_to=None))
    context = {'forums': forums,
               'count': count,
               'discussions': discussions,
               'replies': replies
               }
    return render(request, 'forum.html', context)


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
    forum = Forum.objects.get(item=item)
    discussion = forum.discussion_set.all()
    replies = Discussion.objects.filter(~Q(reply_to=None)).all()
    return render(request, 'item.html', {'item': item, 'forum': forum, 'discussion': discussion, 'replies': replies})


def delivery(request):
    if request.method == 'POST':
        price = float(request.POST['price'])
        order_id = request.POST['order_id']
        Bidfor.objects.create(price=price, delivery_company_id=request.user.id, order_id=order_id)
        messages.info(request, "Success!!!")
        return redirect("/account/")
    else:
        return render(request, 'delivery.html')


def purchase(request, url_slug):
    item = Item.objects.get(url_slug=url_slug)
    customer = Customer.objects.get(id=request.user.id)
    if customer.saved_address == "NULL":
        return render(request, "purchase.html", {'item': item, 'balance': customer.balance})
    else:
        return render(request, "purchase.html",
                      {'item': item, 'balance': customer.balance, 'saved_address': customer.saved_address})


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

            post = request.POST.copy()
            post['address'] = urllib.parse.unquote(request.POST['address'])
            # record transaction
            form = TransactionForm(post)
            transaction = form.save(commit=False)
            transaction.customer = customer
            form.save()

            # record order
            form = OrderForm(post)
            order = form.save(commit=False)
            order.customer = customer
            order.item = item
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
                return redirect("/purchase/" + url_slug)

        # check input balance is enough
        if request.POST['payment_method'] == 'balance':
            if item.price > Customer.objects.get(id=request.user.id).balance:
                messages.info(request, "not enough balance, please topup first")
                return redirect("/purchase/" + url_slug)

            else:
                return render(request, "purchaseConfirm.html", {'item': item,
                                                                'payment_method': request.POST['payment_method'],
                                                                'address': request.POST['address']})

    else:
        return render(request, "purchaseConfirm.html")


def tabooList(request):
    wordlist = list(TabooList.objects.values_list('word', flat=True))
    if request.method == "POST":
        if "word" in request.POST:
            if ' ' in request.POST['word']:
                messages.info(request, "Warning: Space is not allowed!!!")
            else:
                if TabooList.objects.filter(word=request.POST['word'].upper()).exists():
                    messages.info(request, "This word is already in the list.")
                else:
                    TabooList.objects.create(word=request.POST['word'], addBy_id=request.user.id)
                    txt = "The word {word} has been added successfully."
                    messages.info(request, txt.format(word=request.POST['word']))

            return redirect("/taboolist/")

    return render(request, 'tabooList.html', {'word_list': wordlist})


def transaction(request):
    data = Transaction.objects.filter(customer_id=request.user.id)

    return render(request, 'transaction.html', context={'data': data})


def viewOrder(request):
    data = Order.objects.filter(customer_id=request.user.id)
    ## Do not know how to acess data from another table
    return render(request, 'viewOrder.html', context={'data': data})


def changePassword(request):  ## do not have any functionality
    return render(request, 'changePassword.html')


def forum_reply(request):
    if request.method == 'POST':
        if 'discuss' in request.POST:
            message = request.POST['discuss']
            for bad_word in TabooList.objects.values_list('word', flat=True):
                message = re.sub(bad_word, "*" * len(bad_word), message, flags=re.I)
            Discussion.objects.create(user=request.user, forum_id=request.POST['forum_id'], discuss=message,
                                      reply_to=request.POST['discussionID'])
            if message == request.POST['discuss']:
                messages.info(request, "Your reply is submitted!")
            else:
                messages.info(request, "Your reply is submitted!")
                Warning.objects.create(reported_user=request.user, finalized=True, description='__Taboo_List_Auto__')
                messages.info(request, "A warning created since your message contains sensitive word(s)!!!")
            return redirect('/forum/')
        discussion = Discussion.objects.get(id=request.POST["discussionID"])
        context = {'discussion': discussion, 'discussionID': request.POST["discussionID"],
                   'forum_id': request.POST['forum_id']}
        return render(request, 'forumReply.html', context)
    return render(request, 'forumReply.html')


def addDiscussion(request):
    if request.method == 'POST':
        if "discuss" in request.POST:
            message = request.POST['discuss']
            for bad_word in TabooList.objects.values_list('word', flat=True):
                message = re.sub(bad_word, "*" * len(bad_word), message, flags=re.I)
            Discussion.objects.create(user_id=request.user.id, forum_id=request.POST['forum_id'], discuss=message)
            if message == request.POST['discuss']:
                messages.info(request, "Your comments are submitted!")
            else:
                messages.info(request, "Your comments are submitted!")
                Warning.objects.create(reported_user=request.user, finalized=True, description='__Taboo_List_Auto__')
                messages.info(request, "A warning created since your message contains sensitive word(s)!!!")
            return redirect('/forum/')
        context = {'forum_id': request.POST['forum_id']}
        return render(request, 'addDiscussion.html', context)
    else:
        return render(request, 'addDiscussion.html')


def assignDeliCom(request):
    if request.POST:
        companyID = request.POST["deliCompany"]
        orderID = request.POST["orderID"]
        order = Order.objects.get(id=orderID)
        bids = order.bidfor_set.all()
        lowest_price = 99999999
        for bid in bids:
            if bid.price < lowest_price:
                lowest_price = bid.price
        selected = Bidfor.objects.get(order_id=orderID, delivery_company_id=companyID).price
        order.status = 'delivering'
        order.delivery_company_id = companyID
        order.assigned_by_id = request.user.id
        order.save()
        if selected == lowest_price:
            messages.info(request, "Delivery company assigned successfully!")
        else:
            messages.info(request,
                          "Delivery company assigned successfully but you need to provide justification to avoid warning.")
            warning = Warning.objects.create(reported_user=request.user, finalized=True,
                                             description='__Possible_Cheating_Auto__')
            return render(request, 'justification.html', {'orderID': order.id, 'warningID': warning.id})
    open_orders = Order.objects.filter(status='in progress')
    bid_info = []
    for order in open_orders:
        bid_info.append(order.bidfor_set.all())
    context = {"open_orders": open_orders, "bid_info": bid_info}
    return render(request, 'assignDeliCom.html', context)


def justification(request):
    if request.POST:
        if 'order_id' in request.POST:
            orderID = int(request.POST['order_id'])
            cur_order = Order.objects.get(id=orderID)
            justification = request.POST['justification']
            cur_warning = Warning.objects.get(id=request.POST['warning_id'])
            cur_warning.description = cur_warning.description + "           Justification: " + justification
            cur_warning.save()
            cur_order.justification = justification
            cur_order.save()
            justification = justification.strip()
            if justification != '':
                warning = Warning.objects.get(id=request.POST['warning_id'])
                warning.finalized = False
                warning.save()
                messages.info(request, "Your justification has been submitted.")
            else:
                messages.info(request, "Warning created since you fail to provide justification!!!")
            return redirect('/assignDeliCom/')
    return render(request, 'justification.html')


def tracking(request, url_slug):
    order = Order.objects.get(url_slug=url_slug)
    estimate_time = order.transaction.time + datetime.timedelta(days=7)
    context = {'order': order, 'estimate_time': estimate_time}
    return render(request, 'tracking.html', context)


def address(request):
    if request.method == 'GET':
        customer = Customer.objects.get(id=request.user.id)
        if not customer.saved_address:
            return render(request, "address.html")
        else:
            return render(request, "modifyAddress.html")
    else:
        customer = Customer.objects.get(id=request.user.id)
        if not customer.saved_address:
            new_address = request.POST['m_address']
            customer.saved_address = new_address
            customer.save()
            messages.info(request, "Address updated successfully!")
            return redirect('/account/')
        else:
            new_address = request.POST['m_address']
            customer.saved_address = new_address
            customer.save()
            messages.info(request, "Address updated successfully!")
            return redirect('/account/')


def rating(request, url_slug=None):
    order = Order.objects.get(url_slug=url_slug)

    if request.method == 'POST':
        order.item_score = request.POST['item_score']
        order.delivery_score = request.POST['delivery_score']
        order.save()
        order.item.rating = Order.objects.filter(item=order.item).aggregate(avg_item_score=Avg('item_score'))[
            'avg_item_score']
        order.item.save()
        order.delivery_company.rating = Order.objects.filter(delivery_company=order.delivery_company).aggregate(
            avg_delivery_score=Avg('delivery_score'))['avg_delivery_score']
        order.delivery_company.save()
        messages.info(request, "thank you for your rating")
        return redirect('/viewOrder/')

    else:
        return render(request, 'rating.html')


def viewWarning(request):
    data = Warning.objects.filter(reported_user_id=request.user.id)
    context = {'data': data}
    return render(request, "viewWarning.html", context)


# only manager can access this page
def warningJustification(request):
    warning = Warning.objects.filter(finalized=False)
    if request.method == 'POST':
        if 'stay' in request.POST:
            warning = Warning.objects.get(id=request.POST["id"])
            warning.finalized = True
            warning.justification = request.POST['justification']
            warning.save()
            messages.info(request, 'warning stay successful')
            return redirect('/warningJustification/')
        if 'remove' in request.POST:
            Warning.objects.get(id=request.POST['id']).delete()
            messages.info(request, 'warning remove successful')
            return redirect('/warningJustification/')
        if 'revert' in request.POST:
            myid = request.POST["id"]
            if ForumWarning.objects.filter(id=myid).exists():
                warning1 = ForumWarning.objects.get(id=myid)
                reporter = warning1.reporter
                reported = warning1.reported_user
                warning1.reporter = reported
                warning1.reported_user = reporter
                warning1.finalized = True
                warning1.justification = request.POST['justification']
                warning1.save()
                messages.info(request, "Complaint revered successfully ")
            elif OrderWarning.objects.filter(id=myid).exists():
                warning1 = OrderWarning.objects.get(id=myid)
                reporter = warning1.reporter
                reported = warning1.reported_user
                warning1.reporter = reported
                warning1.reported_user = reporter
                warning1.finalized = True
                warning1.justification = request.POST['justification']
                warning1.save()
                messages.info(request, "Complaint revered successfully ")
            else:
                messages.info(request, "You can not reverse this (AUTO)warning generated by the system.")
        return render(request, 'warningJustification.html', {"warning": warning})
    else:
        return render(request, 'warningJustification.html', {"warning": warning})


def ComplaintHistory(request):
    order = OrderWarning.objects.filter(reporter_id=request.user.id)
    forum = ForumWarning.objects.filter(reporter_id=request.user.id)
    context = {'order': order, 'forum': forum}
    return render(request, 'viewComplaint.html', context)


def aboutus(request):
    return render(request, 'aboutus.html')


def rmUser(request):
    return render(request, 'removeUser.html')

def suggestedItem(request):
    if request.method == 'POST':
        form = SuggestedItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'success')
            return redirect('/suggestedItem/')

        else:
            messages.info(request, 'something wrong')
            return redirect('/suggestedItem/')

    else:
        form = SuggestedItemForm()
        return render(request, 'suggestedItem.html', {'form': form})


def provideTracking(request):
    deli_order = Order.objects.filter(Q(delivery_company=request.user) & Q(status='delivering'))
    if request.method == 'POST':
        curr_order = Order.objects.get(id=request.POST['order_id'])
        if 'update' in request.POST:
            if request.POST['tracking'] == "":
                messages.info(request, 'please enter tracking info')

            else:
                curr_order.tracking_info = request.POST['tracking']
                curr_order.save()

        if 'complete' in request.POST:
            curr_order.status = 'complete'
            curr_order.tracking_info = 'complete'
            curr_order.save()

        return redirect('/provideTracking/')

    else:
        return render(request, 'provideTracking.html', {'deli_order': deli_order})

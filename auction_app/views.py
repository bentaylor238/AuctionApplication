import datetime
import random
import string

from django.shortcuts import render
from auction_app.models import Rules, AuctionUser, SilentItem, Bid, Item, Auction
from django.utils import timezone
from .forms import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
# from django.contrib.auth.models import User
#from django.contrib.auth import authenticate



def home(request):
    context={}#data to send to the html page goes here
    return render(request, 'home.html', context)

def live(request):
    context={}#data to send to the html page goes here
    return render(request, 'live.html', context)

def payment(request):
    users = AuctionUser.objects.all()
    context={"users": users}#data to send to the html page goes here
    return render(request, 'payment.html', context)

def rules(request):
    if Rules.objects.count() == 0:
        rules = getDefaultRules()
        rules.save()
    else:
        rules = Rules.objects.get()

    if request.method == "POST":
        form = RulesForm(request.POST, instance=rules) # this way, we save a rules object to the db via a RulesForm
        form.save()
        return redirect(home)
    else:
        form = RulesForm(instance=rules)
        context = {
            "rules": rules,
            "form":form}
        return render(request, 'rules.html', context)

def getDefaultRules():
    f = open('auction_app/static/txt/defaultRules.txt', 'r')
    defaultRules = f.read()
    f.close()
    f = open('auction_app/static/txt/defaultAnnouncements.txt', 'r')
    defaultAnnouncements = f.read()
    f.close()
    return Rules(title="Rules & Announcements",
                last_modified=timezone.now(),
                rules_content=defaultRules,
                announcements_content=defaultAnnouncements)

def createMockItems():
    for i in range(10):
        auction = Auction.objects.all()[0]
        item = SilentItem(title=randomString(), description=randomString(), imageName=randomString(), auction=auction)
        user = AuctionUser.objects.all()[0]
        item.save()
        user.save()
        bid = Bid(amount=0, user=user, item=item)
        bid.save()

def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
                    
def silent(request):

    SilentItem.objects.all().delete()
    Bid.objects.all().delete()

    createMockItems()

    context = {
        'bidform': BidForm(),
        'itembid': getItemBid()
    }
    return render(request, 'silent.html', context)


def getItemBid():
    mylist = []
    # bidlist needs to be a list of bids, one for each item, where the returned bid is is the highest amount for that item
    bidlist = getHighestBid()
    itemlist = list(SilentItem.objects.all())
    for i in range(len(SilentItem.objects.all())):
        mylist.append((bidlist[i], itemlist[i]))
    return mylist


def getHighestBid(): # returns list of one bid per item, where the bid is the highest amount
    list = []
    for item in SilentItem.objects.all():
        bids = Bid.objects.filter(item=item)
        tracker = 0.0
        highestbid = Bid()
        for bid in bids:
            print('$', bid.amount)
            if bid.amount > tracker:
                highestbid = bid
                tracker = highestbid.amount
        list.append(highestbid)
    return list


def submit_bid(request):
    context = {}
    if request.method == 'POST':
        # for key in request.POST:
        #     print('##### ', key, request.POST[key])
        amount = request.POST['amount']
        id = request.POST['item_id']
        # create new form
        bidform = BidForm(request.POST)
        if bidform.is_valid():
            # create a bid object
            # print('USER === ', request.user.username)
            # bid = Bid.objects.get(item=SilentItem.objects.get(id=id))
            new_bid = Bid(item=SilentItem.objects.get(id=id), amount=amount, user=AuctionUser.objects.get(username=request.user.username)) # TODO: get user somehow here
            new_bid.save()
            # bid.amount = amount
            # # bid.user = User.objects.get()
            # bid.user = User.objects.get(name='user2')
            # bid.save()
            context = {
                'bidform': BidForm(),
                'itembid': getItemBid()
            }
        else:
            # this means invalid data was posted
            context = {
                'bidform': bidform,
                'itembid': getItemBid()
            }
    return render(request, 'silent.html', context)

def users(request):
    users = AuctionUser.objects.all()
    userForm = CreateAccount()
    context={"users": users,
             "form": userForm}#data to send to the html page goes here
    return render(request, 'users.html', context)


def afterLogin(request):
    if request.user.is_superuser:
        return redirect(home)
    else:
        return redirect(rules)


def updateAuctionNumber(request):
    #do update
    for key in request.POST:
        print(f"\t{key} => {request.POST[key]}")
    username = request.POST['username']
    user = AuctionUser.objects.get(username=username)
    user.auction_number = request.POST['auction_number']
    user.save()
    return redirect(users)

#LEFT HERE FOR EXAMPLES, AREN'T BEING USED
# def login(request, login_form=Login(), create_account_form=CreateAccount()):
#     if request.method == 'POST':
#         for key in request.GET:
#             print(f"\t{key} => {request.GET[key]}")
#         login_form = Login(request.POST)
#         if login_form.is_valid():
#             return redirect(rules)
#         else:
#             context={
#                 #data to send to the html page goes here
#                 'login_form': login_form, #defaults to a blank Login() object
#                 'create_account_form': create_account_form, #defaults to a blank CreateAccount() object
#                 'loginPage': True
#             }
#             return render(request, 'login.html', context)
#     username = None
#     password = None
#     return render(request, 'login.html', context)


# def create_account(request):

#     if request.method == 'POST':
#         for key in request.POST:
#             print(f"\t{key} => {request.POST[key]}")
#         create_account_form = CreateAccount(request.POST)
#         if create_account_form.is_valid():
#             #create user model and save
#             username = request.POST['new_username']
#             email = request.POST['email']
#             password = request.POST['new_password']
#             firstname = request.POST['first_name']
#             lastname = request.POST['last_name']
#             new_user = User(name=firstname+" "+lastname, username=username, email=email, password=password)
#             new_user.save()
#             print("user created: " + username)
#             return redirect(rules)
#         else:
#             #call the login view passing in the form to render
#             return login(request, create_account_form=create_account_form)

     
class CreateAccount(generic.CreateView):
    form_class = CreateAccount
    success_url = reverse_lazy('afterLogin')
    template_name = 'createAccount.html'

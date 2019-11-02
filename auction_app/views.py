import datetime
import random
import string

from django.shortcuts import render
from auction_app.models import Rule, AuctionUser, SilentItem, Bid, Item, Auction
from django.utils import timezone
from .forms import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from .debug_settings import *

@login_required
def home(request):
    context={}#data to send to the html page goes here
    return render(request, 'home.html', context)

@login_required
def init_test_db(request):
    if DEBUG:
        AuctionUser(
            username="user1",
            password="passpass",
            email="email@email.com",
            first_name="tommy",
            last_name="thompson",
            auction_number=20,
        ).save()
        AuctionUser(
            username="user2",
            password="passpass",
            email="email@email.com",
            first_name="johnny",
            last_name="johnson",
            auction_number=10,
        ).save()
        Rule(title="Rules & Announcements",
                last_modified=timezone.now(),
                rules_content="Insert rules here",
                announcements_content="Insert announcements here"
        ).save()
        silentAuction = Auction(type="silent")
        silentAuction.save()
        liveAuction = Auction(type="live")
        liveAuction.save()
        for i in range(10):
            item = SilentItem(
                title=randomString(), 
                description=randomString(), 
                imageName=randomString(), 
                auction=silentAuction
            )
            item.save()
            user = AuctionUser.objects.all().first()
            user.save()
            bid = Bid(amount=0, user=user, item=item).save()
        return redirect(login)
    else:
        return HttpResponseNotFound()

@login_required
def live(request):
    context={}#data to send to the html page goes here
    return render(request, 'live.html', context)

@login_required
def payment(request):
    users = AuctionUser.objects.all()
    context={"users": users}#data to send to the html page goes here
    return render(request, 'payment.html', context)

@login_required
def rules(request):
    #get a rules object from db or create a blank one
    rules = Rule.objects.all().first()
    empty = False
    if not rules:
        empty = True
        rules = Rule()

    if request.method == "POST":
        if empty:
            form = RulesForm(request.POST) #creates new rules object when saved
        else: 
            form = RulesForm(request.POST, instance=rules) #update the existing rules with post data
        form.save()
        return redirect(home)
    else:
        form = RulesForm(instance=rules) #populate form with db or blank data
        context = {
            "rules": rules,
            "form":form
        }
    return render(request, 'rules.html', context)

def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
       
@login_required                    
def silent(request):

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
    tracker = 0.0
    highestbid = Bid()
    for item in SilentItem.objects.all():
        bids = Bid.objects.filter(item=item)
        for bid in bids:
            if bid.amount > tracker:
                highestbid = bid
        list.append(highestbid)
        tracker = 0.0
    return list

@login_required
def submit_bid(request):
    context = {}
    if request.method == 'POST':
        for key in request.POST:
            print('##### ', key, request.POST[key])
        amount = request.POST['amount']
        id = request.POST['item_id']
        # create new form
        bidform = BidForm(request.POST)
        if bidform.is_valid():
            # create a bid object
            print('USER === ', request.user.username)
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

@login_required
def users(request):
    users = AuctionUser.objects.all()
    userForm = CreateAccountForm()
    context={"users": users,
             "form": userForm}#data to send to the html page goes here
    return render(request, 'users.html', context)

@login_required
def afterLogin(request):
    #login the user
    login(request, request.user)
    if request.user.is_superuser:
        return redirect(home)
    else:
        return redirect(rules)

@login_required
def updateAuctionNumber(request):
    #do update
    for key in request.POST:
        print(f"\t{key} => {request.POST[key]}")
    username = request.POST['username']
    user = AuctionUser.objects.get(username=username)
    user.auction_number = request.POST['auction_number']
    user.save()
    return redirect(users)

#great example of form handling
def create_account(request):
    if request.method == 'POST':
        #create a form object from post data
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            #save data and login the resulting user
            user = form.save()
            login(request, user)
            #redirect to rules view
            return redirect(rules)
        else:
            #form data will be sent back to page because it was invalid
            context = {"form":form}
    else:
        #generates a blank form 
        form = CreateAccountForm()
        context = {"form":form}
    #send back to create account template with the form to render
    return render(request, "CreateAccount.html", {"form":form})
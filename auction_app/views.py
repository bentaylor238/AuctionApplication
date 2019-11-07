import datetime
import random
import string

from django.shortcuts import render
from .models import *
from .forms import *
from django.utils import timezone
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from .debug_settings import *


@login_required
def home(request):
    if request.method == "POST":
        # for key in request.POST:
        #     print(f"\t{key} => {request.POST[key]}")
        request.POST = request.POST.copy() #create a mutable post
        request.POST['published'] = not getBool(request.POST['published'])
        auctionType = request.POST['type']
        auction = Auction.objects.filter(type=auctionType).first()
        form = AuctionForm(request.POST, instance=auction)
        form.save()
    silentAuction = Auction.objects.filter(type='silent').first()
    silentForm = AuctionForm(instance=silentAuction)
    liveAuction = Auction.objects.filter(type='live').first()
    liveForm = AuctionForm(instance=liveAuction)
    auctionForms = [silentForm, liveForm]
    context={"forms":auctionForms} #data to send to the html page goes here
    return render(request, 'home.html', context)

def getBool(str):
    if str.lower() == 'true':
        return True
    else:
        return False

def nukeDB():
    Auction.objects.all().delete()
    SilentItem.objects.all().delete()
    LiveItem.objects.all().delete()
    Rule.objects.all().delete()
    AuctionUser.objects.all().delete()
    # BidSilent.objects.all().delete()
    # BidLive.objects.all().delete()

def init_test_db(request):
    if DEBUG:
        nukeDB()
        AuctionUser.objects.create_user(
            username="user1",
            password="letmepass",
            email="email@email.com",
            first_name="tommy",
            last_name="thompson",
            auction_number=20,
        )
        AuctionUser.objects.create_user(
            username="user2",
            password="letmepass",
            email="email@email.com",
            first_name="johnny",
            last_name="johnson",
            auction_number=10,
        )
        AuctionUser.objects.create_superuser(
            username="admin",
            email="admin@email.com",
            password="letmepass"
        )
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
            # populated the live database too
            itemLive = LiveItem(
                title=randomString(),
                description=randomString(),
                imageName=randomString(),
                auction=silentAuction,
                orderInQueue=i
            )
            itemLive.save()
        return redirect("login")
    else:
        return HttpResponseNotFound()

@login_required
def live(request):
    #this prevents non admins from getting to this page if its not a published auction
    liveAuction = Auction.objects.filter(type='live').first()
    if not liveAuction.published and not request.user.is_superuser:
        return redirect(home)

    createItemForm = LiveItemForm(initial={'auction':liveAuction})

    try:
        Auction.objects.get(type='live')
    except Exception as e:
        return HttpResponse("The live auction object does not yet exist. Create a live auction then try again. Django error message is " + str(e))

    try:
        currentItem = LiveItem.objects.filter(sold='False').order_by('orderInQueue')[0]
        context = {
            'currentItem': currentItem,
            'published': liveAuction.published,
            'items': LiveItem.objects.all().filter(sold=False).exclude(pk=currentItem.pk),
            "createItemForm":createItemForm,
        }
        return render(request, 'live.html', context)
    except Exception as e:
        return HttpResponse("Error (there are probably more than one items in the database with an orderInQueue equal to 1. Here's the full error from django: " + str(e))

def sellLiveItem(request):
    soldItem = LiveItem.objects.get(pk=request.POST['pk'])
    try:
        amount = request.POST['amount']
        user = AuctionUser.objects.get(auction_number=request.POST['auctionNumber'])
        bid = BidLive(amount=amount, user=user, item=soldItem)
        bid.save()
        soldItem.sold = True
        soldItem.save()
        return redirect(live)
    except Exception as e:
        context = {
            'item': soldItem,
            'error': e,
            'auctionNumber': request.POST['auctionNumber']
        }
        return render(request, 'liveErrorMessage.html', context)


@login_required
def payment(request):
    users = AuctionUser.objects.all()
    for user in users:
        user.amount = 0
    bids = BidSilent.objects.all()
    for bid in bids:
        bid.user.amount += bid.amount
    context={"users": users}#data to send to the html page goes here
    return render(request, 'payment.html', context)

def updateUserPayment(request):
    username = request.POST['username']
    user = AuctionUser.objects.get(username=username)
    for var in request.POST:
        print(var)
    if 'paid' in request.POST:
        user.has_paid = True
    else:
        user.has_paid = False
    user.save()
    return redirect(payment)

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
def create_item(request):
    if request.method == "POST" and request.user.is_superuser:
        for key in request.POST:
            print(f"\t{key} => {request.POST[key]}")
        request.POST = request.POST.copy() #make the post mutable
        auctionType = request.POST.get('type', "")
        
        # auction = Auction.objects.filter(type=auctionType).first()
        # request.POST['auction'] = auction
        
        if auctionType =='silent':
            #format the date time input
            if request.POST.get('end'):
                request.POST['end'] = datetime.datetime.strptime(request.POST['end'], '%Y-%m-%dT%H:%M')
            else:
                request.POST['end'] = None
            item = SilentItemForm(request.POST)
        elif auctionType == 'live':
            item = LiveItemForm(request.POST)

        #check if valid before saving
        if item.is_valid():
            item.save()
        else:
            print("invalid item")

        if auctionType == 'silent':
            return redirect(silent) 
        elif auctionType == 'live':
            return redirect(live)
    else:
        #not authorized to make request
        return HttpResponseForbidden()

@login_required                    
def silent(request):
    #this prevents non admins from getting to this page if its not a published auction
    silentAuction = Auction.objects.filter(type='silent').first()
    if not silentAuction.published and not request.user.is_superuser:
        return redirect(home)

    winning, bidon, unbid = getBidItemForm(request)
    createItemForm = SilentItemForm(initial={'auction':silentAuction})

    context = {
        'published': silentAuction.published,
        'createItemForm': createItemForm,
        'winning': winning,
        'bidon': bidon,
        'unbid': unbid
    }
    return render(request, 'silent.html', context)


def getBidItemForm(request):
    winning = []
    bidon = []
    unbid = []
    for item in SilentItem.objects.all():
        if item.bidsilent_set:
            winningbid = item.bidsilent_set.order_by("amount").last()
            if item.bidsilent_set.filter(user__username=request.user.username).count() > 0:
                # there is a bid for that user
                if winningbid.user.username == request.user.username:
                    # the user is the winning user
                    # winningbid is a bid
                    # item is the item
                    winning.append((winningbid.amount, item, BidForm(initial={'amount': winningbid.amount})))
                else:
                    # the user has a bid but its not winning
                    bidon.append((winningbid.amount, item, BidForm(initial={'amount': winningbid.amount})))
            else:
                # this means there is a bid for the item, but the current user has not bid on it
                unbid.append((0, item, BidForm(initial={'amount': 0})))
        else:
            # there is no bid associated with the item
            unbid.append((0, item, BidForm(initial={'amount': 0})))
    return winning, bidon, unbid


@login_required
def submit_bid(request):
    if request.method == 'POST':
        # for key in request.POST:
        #     print('#####', key, request.POST[key])
        amount = request.POST['amount']
        id = request.POST['item_id']
        bidform = BidForm(request.POST)
        if bidform.is_valid():
            currentitem = SilentItem.objects.get(id=id)
            if currentitem.bidsilent_set.count() > 0:
                if float(amount) > currentitem.bidsilent_set.order_by("amount").last().amount:
                    new_bid = BidSilent(item=currentitem, amount=amount, user=AuctionUser.objects.get(username=request.user.username))
                    new_bid.save()
            else:
                # this means there were no bids, create a new one
                new_bid = BidSilent(item=currentitem, amount=amount, user=AuctionUser.objects.get(username=request.user.username))
                new_bid.save()
        else:
            # this means invalid data was posted
            print("invalid data")

    return HttpResponseRedirect("/silent")


@login_required
def users(request):
    users = AuctionUser.objects.all()
    form = CreateAccountForm()
    print(form.fields)
    form.fields['password1'].widget = forms.HiddenInput()
    form.initial['password1'] = "ax7!bwaZc"
    form.fields['password2'].widget = forms.HiddenInput()
    form.initial['password2'] = "ax7!bwaZc"
    if request.method == 'POST':
        form_data = request.POST.copy()
        form_data.update(password1="ax7!bwaZc")
        form_data.update(password2="ax7!bwaZc")
        form = CreateAccountForm(form_data)
        # print(form.is_valid())
        if form.is_valid():
            #save data
            form.save()
            users = AuctionUser.objects.all()
            form = CreateAccountForm()
            context = {
                "users": users,
                "form": form
            }
            return render(request, 'users.html', context)
        else:
            context = {
                "users": users,
                "form":form}
            # print(form.cleaned_data)
            # print(form.errors) #NEED TO PRINT SOME ERRORS TO THE USER SOMEHOW
            return render(request, 'users.html', context)
    else:
        #first visit
        context={"users": users,
                 "form": form}#data to send to the html page goes here
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
            print(form.cleaned_data)
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

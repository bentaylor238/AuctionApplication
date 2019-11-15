import datetime
import random
import string

from django.shortcuts import render
from .models import *
from .forms import *
from django.utils import timezone
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
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

    user = request.user
    user.amount = 0
    user.items = []
    userBids = BidSilent.objects.filter(user__id=user.id)
    for bid in userBids:
        if bid.isWinning:
            user.amount+=bid.amount
    liveItems = LiveItem.objects.filter(user__id=user.id)
    for item in liveItems:
        user.amount+=item.amount
        user.items.append(item)
    print(user.amount)
    user.save()

    auctionTotalWinnings = 0
    silentItemBids = BidSilent.objects.all()
    for bid in silentItemBids:
        if bid.isWinning:
            auctionTotalWinnings += bid.amount

    liveItems = LiveItem.objects.all()
    for item in liveItems:
        if item.sold:
            auctionTotalWinnings+=item.amount
    context={"forms":auctionForms,
             "user": user,
             "totalWinnings": auctionTotalWinnings} #data to send to the html page goes here
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
            new_bid = BidSilent(item=item, amount=12.00, user=AuctionUser.objects.get(auction_number=20))
            new_bid.save()
            # populated the live database too
            itemLive = LiveItem(
                title=randomString(),
                description=randomString(),
                imageName=randomString(),
                auction=silentAuction,
            )
            itemLive.user = AuctionUser.objects.get(auction_number=10)
            itemLive.amount = 10.00
            itemLive.sold = True
            itemLive.save()
        return redirect("login")
    else:
        return HttpResponseNotFound()

@login_required
def delete_item(request):
    if request.method == "POST" and request.user.is_superuser:
        auctionType = request.POST.get('type', "")
        pk = request.POST.get('pk',None)
        if auctionType == "silent":
            items = SilentItem.objects
        elif auctionType == "live":
            items = LiveItem.objects
        else:
            return HttpResponseServerError()
        items.get(pk=pk).delete()
        return redirect(auctionType)
    return HttpResponseNotFound()


@login_required
def live(request):
    # this prevents non admins from getting to this page if its not a published auction
    liveAuction = Auction.objects.filter(type='live').first()

    # perform check to validate proper initialization
    if not liveAuction.published and not request.user.is_superuser:
        return redirect(home)
    if len(AuctionUser.objects.filter(auction_number=-1)) == 0: # optimize by initializing in the init function instead of calling it every time
        defaultUser = AuctionUser(auction_number=-1, has_paid=True, amount=0)
        defaultUser.save()
    try:
        Auction.objects.get(type='live')
    except Exception as e:
        return HttpResponse("The live auction object does not yet exist. Create a live auction then try again. Django error message is " + str(e))

    # functionality
    createItemForm = LiveItemForm(initial={'auction':liveAuction})
    currentItem = LiveItem.objects.filter(sold='False').order_by('pk').first()
    if liveAuction.published:
        items = LiveItem.objects.all().exclude(pk=currentItem.pk)
    else:
        items = LiveItem.objects.all()
    context = {
        'currentItem': currentItem,
        'published': liveAuction.published,
        'items': items,
        'createItemForm':createItemForm,
    }
    return render(request, 'live.html', context)



def sellLiveItem(request):
    soldItem = LiveItem.objects.get(pk=request.POST['pk'])
    try:
        soldItem.user=AuctionUser.objects.get(auction_number=request.POST['auction_number'])
        soldItem.amount = request.POST['amount']
        soldItem.sold = True
        soldItem.save()
        return redirect(live)
    except Exception as e:
        context = {
            'item': soldItem,
            'error': e,
            'auctionNumber': request.POST['auction_number']
        }
        return render(request, 'liveErrorMessage.html', context)


@login_required
def payment(request):
    users = AuctionUser.objects.all()
    for user in users:
        user.amount = 0.0
        user.items = []
        # for silent
        bids = BidSilent.objects.filter(user__id=user.id)
        for bid in bids:
            if bid.isWinning:
                user.amount += bid.amount
                # print(bid.user, bid.amount)

        # for live
        items = LiveItem.objects.filter(user__id=user.id)
        for item in items:
            user.amount += item.amount
            user.items.append(item)
            # print(item.amount, item.user)
        user.save()
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

    winning, bidon, unbid = getItemLists(request)
    createItemForm = SilentItemForm(initial={'auction':silentAuction})

    context = {
        'published': silentAuction.published,
        'createItemForm': createItemForm,
        'winning': winning,
        'bidon': bidon,
        'unbid': unbid
    }
    return render(request, 'silent.html', context)


def getItemLists(request):
    winning = []
    bidon = []
    unbid = []
    for item in SilentItem.objects.all():
        if item.bidsilent_set.count() > 0:
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
                unbid.append((winningbid.amount, item, BidForm(initial={'amount': winningbid.amount})))
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
        if float(amount) > 0:
            if bidform.is_valid():
                currentitem = SilentItem.objects.get(id=id)
                if currentitem.bidsilent_set.count() > 0:
                    if float(amount) > currentitem.bidsilent_set.order_by("amount").last().amount:
                        # make the new bid the winning bid and the last bid notwinning
                        oldbid = currentitem.bidsilent_set.order_by("amount").last()
                        oldbid.isWinning = False
                        oldbid.save()
                        print('&&&&&', type(oldbid))
                        new_bid = BidSilent(item=currentitem, amount=amount, user=AuctionUser.objects.get(username=request.user.username), isWinning=True)
                        new_bid.save()
                else:
                    # this means there were no bids, create a new one
                    new_bid = BidSilent(item=currentitem, amount=amount, user=AuctionUser.objects.get(username=request.user.username), isWinning=True)
                    new_bid.save()
            else:
                # this means invalid data was posted
                print("invalid data")

    return HttpResponseRedirect("/silent")


@login_required
def users(request):
    users = AuctionUser.objects.all()
    form = CreateAccountFormHiddenPass()
    if request.method == 'POST':
        #set password fields
        form_data = request.POST.copy()
        form_data.update(password1="ax7!bwaZc")
        form_data.update(password2="ax7!bwaZc")
        #fill form with data
        form = CreateAccountFormHiddenPass(form_data)
        if form.is_valid():
            #save data
            form.save()
            return redirect("users")
        else:
            #invalid post
            context = {
                "users": users,
                "form":form}
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
    if user.is_valid():
        user.save()
    


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

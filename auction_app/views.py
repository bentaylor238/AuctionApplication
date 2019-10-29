import datetime

from django.shortcuts import render
from auction_app.models import Rules, User, SilentItem, Bid
from django.utils import timezone
from .forms import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
#from django.contrib.auth.models import User
#from django.contrib.auth import authenticate



def home(request):
    context={'admin':True}#data to send to the html page goes here
    return render(request, 'home.html', context)

def live(request):
    context={}#data to send to the html page goes here
    return render(request, 'live.html', context)

def login(request):
    context={'loginPage': True}#data to send to the html page goes here
    return render(request, 'login.html', context)

def payment(request):
    context={}#data to send to the html page goes here
    return render(request, 'payment.html', context)

def rules(request):
    if Rules.objects.count() == 0:
        setDefaultRules()
    context = {
        "admin":True,
        "rules": Rules.objects.all().get(pk=1),
        "form":RulesForm()}
    return render(request, 'rules.html', context)

def setDefaultRules():
    f = open('auction_app/static/txt/defaultRules.txt', 'r')
    defaultRules = f.read()
    f.close()
    f = open('auction_app/static/txt/defaultAnnouncements.txt', 'r')
    defaultAnnouncements = f.read()
    f.close()
    rules = Rules(title="Rules & Announcements",
                  lastModified=timezone.now(),
                  rulesContent=defaultRules,
                  announcementsContent=defaultAnnouncements
                  )
    rules.save()

def silent(request):

    b = SilentItem(title='log', description='a nice big log', imageName='alogpic', start=datetime.datetime.now())
    a = SilentItem(title='feet', description='a pair of feet', imageName='feets', start=datetime.datetime.now())
    c = SilentItem(title='nothing', description='a whole lot of nothing', imageName='nullspace', start=datetime.datetime.now())
    d = SilentItem(title='taco', description='a little old but edible', imageName='tacopic', start=datetime.datetime.now())
    b.save()
    a.save()
    c.save()
    d.save()

    items = SilentItem.objects.all()
    # bids = Bid.objects.filter(item=SilentItem)

    context={
        'items': items
    }#data to send to the html page goes here
    return render(request, 'silent.html', context)

def users(request):
    context={}#data to send to the html page goes here
    return render(request, 'users.html', context)

def login(request):
    context={
        #data to send to the html page goes here
        'create_account_form': CreateAccount(),
    }
    for key in request.GET:
        print(f"\t{key} => {request.GET[key]}")

    uname = None
    psw = None

    if 'username' in request.GET:
        uname = request.GET['username']
    else:
        return render(request, 'login.html', context)
    if 'password' in request.GET:
        psw = request.GET['password']
    else:
        return render(request, 'login.html', context)

    try:
        user = User.objects.get(username=uname)
    except:
        return render(request, 'login.html', context)
        #return JsonResponse({'error': 'The given username is not in our database :('})

    if user.password == psw:
        return redirect(rules)
    else:
        return render(request, 'login.html', context)
        #return JsonResponse({'error': 'The given password does not match the username :('})

    """
        user = authenticate(username=username, password=password)
        if user is not None:
            # User is authenticated
        else:
            # No user exists
    """

def create_account(request):
    for key in request.POST:
        print(f"\t{key} => {request.POST[key]}")

    username = None
    firstname = ''
    lastname = ''
    email = None
    password1 = None
    password2 = None

    if 'username' in request.POST:
        username = request.POST['username']
    else:
        return redirect(login)
    if 'email' in request.POST:
        email = request.POST['email']
    else:
        return redirect(login)

    if 'password' in request.POST:
        password1 = request.POST['password']
    else:
        return redirect(login)
    if 'confirm_password' in request.POST:
        password2 = request.POST['confirm_password']
    else:
        return redirect(login)
    if 'first_name' in request.POST:
        firstname = request.POST['first_name']
    if 'last_name' in request.POST:
        lastname = request.POST['last_name']
    

    if password1 == password2 and password1 != None:
        new_user = User(name=firstname+" "+lastname, username=username, email=email, password=password1)
        new_user.save()
        print("user created: " + username)
        return redirect(rules)
        '''try:
            user = User.objects.create_user(username, email=username,password=password1)
            user.save()
        except:
            print("Something went wrong in creating the user")
            # no idea at the moment how to handle
    #not sure how to handle any of the else statements yet
'''


def submit_bid(request):
    amount = None
    for key in request.POST:
        print(f"\t{key} => {request.POST[key]}")

    if 'amount' in request.POST:
        amount = request.POST['amount']

    if amount is not None:
        new_bid = Bid(amount=amount)
        new_bid.save()
    return redirect(silent)
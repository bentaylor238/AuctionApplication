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
    context={}#data to send to the html page goes here
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

    b = SilentItem(title='trampoline', description='a nice big trampoline', imageName='tramppic')
    a = SilentItem(title='basketball', description='a flat basketball', imageName='ballpic')
    c = SilentItem(title='nothing', description='a whole lot of nothing', imageName='nullspace')
    d = SilentItem(title='taco', description='a little old but edible', imageName='tacopic')
    b.save()
    a.save()
    c.save()
    d.save()

    items = SilentItem.objects.all()
    # bids = Bid.objects.filter(item=SilentItem)

    context={
        'bidform': BidForm(),
        'items': items
    }#data to send to the html page goes here
    return render(request, 'silent.html', context)

def submit_bid(request):
    context = {}
    if request.method == 'POST':
        # for key in request.POST:
        #     print(f"\t{key} => {request.GET[key]}")
        for key in request.POST:
            print(' ##### ', key)
        amount = request.POST['amount']
        # id = request.POST['item_id']
        # create new form
        bid = BidForm(request.POST)
        if bid.is_valid():
            # create a bid object
            # item = SilentItem.objects.get(id=id)
            item = SilentItem(title='filler', description='filler', imageName='filler')
            user = User()
            user.save()
            item.save()
            new_bid = Bid(amount=amount, item=item, user=user)
            new_bid.save()
            context = {
                # 'bid': new_bid,
                'bidform': BidForm(),
                'items': SilentItem.objects.all()
            }
        else:
            # this means invalid data was posted
            context = {
                # 'bid': Bid(),
                'bidform': bid,
                'items': SilentItem.objects.all()
            }
    return render(request, 'silent.html', context)

def users(request):
    context={}#data to send to the html page goes here
    return render(request, 'users.html', context)

def login(request, login_form=Login(), create_account_form=CreateAccount()):
    context={
        #data to send to the html page goes here
        'login_form': login_form,
        'create_account_form': create_account_form,
        'loginPage': True
    }
    for key in request.GET:
        print(f"\t{key} => {request.GET[key]}")

    username = None
    password = None
    return render(request, 'login.html', context)

    # if 'username' in request.GET:
    #     username = request.GET['username']
    # else:
    #     return render(request, 'login.html', context)
    # if 'password' in request.GET:
    #     password = request.GET['password']
    # else:
    #     return render(request, 'login.html', context)

    # try:
    #     user = User.objects.get(username=username)
    # except:
    #     return render(request, 'login.html', context)
    #     #return JsonResponse({'error': 'The given username is not in our database :('})

    # if user.password == password:
    #     return redirect(rules)
    # else:
    #     return render(request, 'login.html', context)
    #     #return JsonResponse({'error': 'The given password does not match the username :('})

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

    if request.method == 'POST':
        create_account_form = CreateAccount(request.POST)
        if create_account_form.is_valid():
            username = request.POST['new_username']
            email = request.POST['email']
            password = request.POST['new_password']
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            new_user = User(name=firstname+" "+lastname, username=username, email=email, password=password)
            new_user.save()
            print("user created: " + username)
            return redirect(rules)
        else:
            #call the login view passing in the form to render
            return login(request, create_account_form=create_account_form)
            


    if 'new_username' in request.POST:
        username = request.POST['new_username']
    else:
        return redirect(login)
    if 'email' in request.POST:
        email = request.POST['email']
    else:
        return redirect(login)

    if 'new_password' in request.POST:
        password1 = request.POST['new_password']
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
    #not sure how to handle any of the else statements yet'''
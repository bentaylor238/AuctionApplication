from django.shortcuts import render
from auction_app.models import Rules, User
from django.utils import timezone
from .forms import RulesForm
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
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
    context={}#data to send to the html page goes here
    return render(request, 'silent.html', context)

def users(request):
    context={}#data to send to the html page goes here
    return render(request, 'users.html', context)

def login(request):
    context={}#data to send to the html page goes here
    for key in request.GET:
        print(f"\t{key} => {request.GET[key]}")

    uname = None
    psw = None

    if 'username' in request.GET:
        uname = request.GET['username']
    else:
        return HttpResponseRedirect(reverse('auction_app:login'))
    if 'password' in request.GET:
        psw = request.GET['password']
    else:
        return HttpResponseRedirect(reverse('auction_app:login'))

    try:
        user = User.objects.get(username=uname)
    except:
        return HttpResponseRedirect(reverse('auction_app:login'))
        #return JsonResponse({'error': 'The given username is not in our database :('})

    if user.password == psw:
        return HttpResponseRedirect(reverse('auction_app:rules'))
    else:
        return  HttpResponseRedirect(reverse('auction_app:login'))
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
    email = None
    password1 = None
    password2 = None

    if 'uname' in request.POST:
        username = request.POST['uname']
    else:
        return HttpResponseRedirect(reverse('auction_app:login'))
    if 'email' in request.POST:
        email = request.POST['email']
    else:
        return HttpResponseRedirect(reverse('auction_app:login'))

    if 'password1' in request.POST:
        password1 = request.POST['password1']
    else:
        return HttpResponseRedirect(reverse('auction_app:login'))
    if 'password2' in request.POST:
        password2 = request.POST['password2']
    else:
        return HttpResponseRedirect(reverse('auction_app:login'))

    if password1 == password2 and password1 != None:
        new_user = User(username=username, email=email, password=password1,)
        new_user.save()
        return HttpResponseRedirect(reverse('auction_app:rules'))
        '''try:
            user = User.objects.create_user(username, email=username,password=password1)
            user.save()
        except:
            print("Something went wrong in creating the user")
            # no idea at the moment how to handle
    #not sure how to handle any of the else statements yet
'''
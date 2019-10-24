from django.shortcuts import render
from auction_app.models import Rules, User
from django.utils import timezone
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse



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
    context = {"rules": Rules.objects.all().get(pk=1)}
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

    username = None
    password = None

    if 'username' in request.GET:
        username = request.GET['username']
    if 'password' in request.GET:
        password = request.GET['password']

    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse({'error': 'The given username is not in our database :('})

    if user.password == password:
        return HttpResponseRedirect(reverse('auction_app:rules'))
    else:
        return JsonResponse({'error': 'The given password does not match the username :('})

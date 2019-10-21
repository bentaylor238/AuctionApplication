from django.shortcuts import render
from auction_app.models import Rules
from django.utils import timezone

def index(request):
    context={}
    return render(request, 'index.html', context)

def live(request):
    context={}
    return render(request, 'live.html', context)

def login(request):
    context={}
    return render(request, 'login.html', context)

def payment(request):
    context={}
    return render(request, 'payment.html', context)

def rules(request):
    if Rules.objects.count() == 0:
        setDefaultRules()
    context = {"rules": Rules.objects.all().get(pk=1)}
    return render(request, 'rules.html', context)

def setDefaultRules():
    f = open('auction_app/static/auction_app/defaultRules.txt', 'r')
    defaultRules = f.read()
    f.close()
    f = open('auction_app/static/auction_app/defaultAnnouncements.txt', 'r')
    defaultAnnouncements = f.read()
    f.close()
    rules = Rules(title="Rules & Announcements",
                  lastModified=timezone.now(),
                  rulesContent=defaultRules,
                  announcementsContent=defaultAnnouncements
                  )
    rules.save()

def silent(request):
    context={}
    return render(request, 'silent.html', context)

def users(request):
    context={}
    return render(request, 'users.html', context)
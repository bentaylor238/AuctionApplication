from django.shortcuts import render


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
    context={}
    return render(request, 'rules.html', context)

def silent(request):
    context={}
    return render(request, 'silent.html', context)

def users(request):
    context={}
    return render(request, 'users.html', context)
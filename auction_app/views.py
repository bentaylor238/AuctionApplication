from django.shortcuts import render


def index(request):
    context={}
    return render(request, 'auction_app/index.html', context)

def live(request):
    context={}
    return render(request, 'auction_app/live.html', context)

def login(request):
    context={}
    return render(request, 'auction_app/login.html', context)

def payment(request):
    context={}
    return render(request, 'auction_app/payment.html', context)

def rules(request):
    context={}
    return render(request, 'auction_app/rules.html', context)

def silent(request):
    context={}
    return render(request, 'auction_app/silent.html', context)

def users(request):
    context={}
    return render(request, 'auction_app/users.html', context)